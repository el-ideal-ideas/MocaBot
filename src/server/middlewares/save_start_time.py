# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from time import time

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def save_start_time(request: Request):
    """Save start time info to request."""
    request.ctx.start_time = time()

# -------------------------------------------------------------------------- Middleware --
