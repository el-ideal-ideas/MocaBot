# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.exceptions import Forbidden, abort
from limits import parse_many
from asyncio import sleep
from sanic.response import text
from ... import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def api_key_checker(request: Request):
    """A api-key filter."""
    if request.method.upper() == 'OPTIONS':
        return text('success.')
    if not request.raw_url.startswith(b'/static') and \
            not request.raw_url.startswith(b'/web') and \
            not request.raw_url.startswith(b'/status') and \
            request.method.upper() != 'OPTIONS':
        received_key = mzk.get_args(request, ('api_key', str, None, {'max_length': 1024}))[0]
        ip = mzk.get_remote_address(request)
        if received_key is None:
            raise Forbidden('Missing API-KEY.')
        found = False
        for api_key_info in request.app.api_key_config.list:
            if api_key_info.get('key') == received_key:  # found a api key.
                found = True
                if api_key_info.get('status', False):  # check api key status.
                    rate_limit = api_key_info.get('rate')
                    if rate_limit != '*':
                        for item in parse_many(rate_limit):  # check rate limit.
                            if not request.app.rate_limiter.hit(item, received_key):
                                abort(429, 'Too many requests.')
                    else:
                        pass  # '*' means unlimited.
                    allowed = False
                    target = request.raw_url.decode()
                    for path_info in api_key_info.get('allowed_path'):
                        if ':' in path_info:
                            path, path_rate = path_info.split(':')
                        else:
                            path, path_rate, = path_info, '*'
                        if target.startswith(path):
                            if path_rate == '*':
                                allowed = True
                            else:
                                for item in parse_many(path_rate):  # check rate limit.
                                    if not request.app.rate_limiter.hit(item, f'{received_key}-{ip}-{path}'):
                                        abort(429, 'Too many requests.')
                                allowed = True
                            break

                    if not allowed:
                        raise Forbidden("Your API-KEY can't access to this path.")
                    else:
                        pass  # allowed
                    ip = mzk.get_remote_address(request)
                    if api_key_info.get('ip') != '*' and ip not in api_key_info.get('ip'):
                        raise Forbidden(f"Your API-KEY can't use from this ip address. ({ip})")
                    else:
                        pass  # allowed
                    required = api_key_info.get('required')
                    for key, value in required['headers'].items():
                        if request.headers.get(key) != value:
                            raise Forbidden('Missing required header.')
                    for key, value in required['args'].items():
                        if mzk.get_args(request, key)[0] != value:
                            raise Forbidden('Missing required argument.')
                    if api_key_info.get('delay', 0) != 0:
                        await sleep(api_key_info.get('delay'))

                    # --- success. do nothing. ---

                else:
                    raise Forbidden('Your API-KEY is not online.')
                break
        if not found:
            ip = mzk.get_remote_address(request)
            request.app.secure_log.write_log(
                f"Received a unknown API-KEY: <{received_key}> from {ip}.",
                mzk.LogLevel.WARNING
            )
            if request.app.dict_cache.get('unknown_api_key') is None:
                request.app.dict_cache['unknown_api_key'] = {}
            try:
                request.app.dict_cache['unknown_api_key'][ip] += 1
            except KeyError:
                request.app.dict_cache['unknown_api_key'][ip] = 1
            if request.app.dict_cache['unknown_api_key'][ip] > request.app.system_config.get(
                    'block_ip_when_received_invalid_system_auth', int, 0
            ):
                request.app.ip_blacklist.append(ip)
                request.app.secure_log.write_log(
                    f"Add {ip} to the blacklist. <api_key_checker>",
                    mzk.LogLevel.WARNING
                )
            raise Forbidden('Unknown API-KEY.')

# -------------------------------------------------------------------------- Middleware --
