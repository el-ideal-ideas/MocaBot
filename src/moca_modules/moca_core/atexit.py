# this will be executed at system exit.

# -- Imports --------------------------------------------------------------------------

from .moca_variables import IS_DEBUG

# -------------------------------------------------------------------------- Imports --

# -- At Exit --------------------------------------------------------------------------

if IS_DEBUG:
    print(f'------ Moca Modules try exit. ------')

# load at exit file.
from ..moca_data import atexit as _

# -------------------------------------------------------------------------- At Exit --
