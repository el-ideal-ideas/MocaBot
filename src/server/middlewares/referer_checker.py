# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.exceptions import Forbidden
from ... import moca_modules as mzk
from ... import core

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def referer_checker(request: Request):
    """Check the referer header."""
    if not request.raw_url.startswith(b'/status'):
        config = request.app.system_config.get_config('referer', dict)
        # {
        #     "force": bool,
        #     "allowed_referer": []
        # }
        referer = request.headers.get('referer')
        if referer is None and config['force']:
            raise Forbidden('Missing referer.')
        elif referer is not None:
            status = False
            if '*' in config['allowed_referer']:
                status = True
            else:
                for item in config['allowed_referer']:
                    if referer.startswith(item):
                        status = True
                        break
            if not status:
                if core.SERVER_CONFIG.get('debug', False):
                    mzk.print_warning(f'Received a request from unknown referer <{referer}>.')
                raise Forbidden('Invalid referer.')

# -------------------------------------------------------------------------- Middleware --
