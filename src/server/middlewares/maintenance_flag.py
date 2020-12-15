# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.exceptions import abort
from ... import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def maintenance_flag(request: Request):
    """If the maintenance mode is on, Return 503."""
    if mzk.get_remote_address(request) not in request.app.system_config.get_config(
            'maintenance_mode_whitelist', list, ['127.0.0.1']
    ) and request.app.system_config.get_config('maintenance_mode', bool, False):
        abort(503, 'MocaSystem is currently undergoing maintenance.')

# -------------------------------------------------------------------------- Middleware --
