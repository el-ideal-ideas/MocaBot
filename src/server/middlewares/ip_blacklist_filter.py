# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.exceptions import Forbidden
from ... import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def ip_blacklist_filter(request: Request):
    """
    Block all IPs in configs/ip_blacklist.json
    """
    if request.app.ip_blacklist.is_in(mzk.get_remote_address(request)):
        raise Forbidden("Your access was blocked by ip filter.")
    else:
        pass  # do nothing


# -------------------------------------------------------------------------- Middleware --
