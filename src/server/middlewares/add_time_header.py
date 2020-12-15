# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.response import HTTPResponse
from time import time

# -------------------------------------------------------------------------- Imports --

# -- Middleware --------------------------------------------------------------------------


async def add_time_header(request: Request, response: HTTPResponse):
    """Add Start-Time, End-Time, Spent-Time headers to response."""
    try:
        start = request.ctx.start_time
        end = time()
        response.headers.update({
            'Moca-Start-Time': start,
            'Moca-End-Time': end,
            'MocaSpent-Time': end - start,
        })
    except AttributeError:
        pass

# -------------------------------------------------------------------------- Middleware --
