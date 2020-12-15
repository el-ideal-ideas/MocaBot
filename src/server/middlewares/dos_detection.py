"""
This middleware will detect dos attack, and put attacker ip to blacklist.
"""

# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from ... import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def dos_detection(request: Request):
    """Count access for dos detection."""
    ip = mzk.get_remote_address(request)
    if request.app.dict_cache.get('dos-detect') is None:
        request.app.dict_cache['dos-detect'] = {}
    try:
        request.app.dict_cache['dos-detect'][ip] += 1
    except KeyError:
        request.app.dict_cache['dos-detect'][ip] = 1

# -------------------------------------------------------------------------- Middleware --
