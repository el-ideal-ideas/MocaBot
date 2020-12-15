# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.exceptions import Forbidden
from ... import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- Utils --------------------------------------------------------------------------


def check_root_pass(request: Request) -> None:
    root_pass, *_ = mzk.get_args(request, ('root_pass', str, None, {'max_length': 1024}))
    if root_pass != request.app.system_config.get_config('root_pass'):
        raise Forbidden('Invalid root password.')

# -------------------------------------------------------------------------- Utils --
