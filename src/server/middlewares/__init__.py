# -- Imports --------------------------------------------------------------------------

from typing import (
    Dict, Callable, Tuple, Union
)
from spf import SanicPlugin
from ... import core
from .ip_blacklist_filter import ip_blacklist_filter
from .maintenance_flag import maintenance_flag
from .force_headers import force_headers
from .api_key_checker import api_key_checker
from .dos_detection import dos_detection
from .referer_checker import referer_checker
from .add_time_header import add_time_header
from .save_start_time import save_start_time

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

request: str = 'request'
response: str = 'response'
plugin: str = 'plugin'

# -------------------------------------------------------------------------- Variables --

# -- Default Middlewares --------------------------------------------------------------------------

middlewares: Dict[str, Tuple[str, Union[Callable, SanicPlugin]]] = {
    'save_start_time': (request, save_start_time),
    'maintenance_flag': (request, maintenance_flag),
    'force_headers': (request, force_headers),
    'referer_checker': (request, referer_checker),
    'api_key_checker': (request, api_key_checker),
    'dos_detection': (request, dos_detection),
    'add_time_header': (response, add_time_header),
}


if core.SERVER_CONFIG['pyjs_secret'] is not None:
    from .moca_encryption import encryption_plugin
    middlewares['encryption_plugin'] = (plugin, encryption_plugin)

# -------------------------------------------------------------------------- Default Middlewares --
