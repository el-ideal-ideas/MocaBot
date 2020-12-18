# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.exceptions import Forbidden
from sanic.response import text

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def force_headers(request: Request):
    """If the request is not contained all headers in `force_headers`, block it."""
    if request.method.upper() == 'OPTIONS':
        return text('success.')
    if not request.raw_url.startswith(b'/static') and \
            not request.raw_url.startswith(b'/web') and \
            not request.raw_url.startswith(b'/status') and \
            request.method.upper() != 'OPTIONS':
        headers = request.app.system_config.get_config('force_headers', dict, {})
        if len(headers) != 0:
            for key, value in headers.items():
                if value is None and request.headers.get(key, None) is not None:
                    pass  # do nothing
                elif request.headers.get(key) != value:
                    raise Forbidden('Missing required header, your request was blocked.')
        else:
            pass  # do nothing.

# -------------------------------------------------------------------------- Middleware --
