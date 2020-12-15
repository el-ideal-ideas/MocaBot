# This file will be loaded at first.

# -- Imports --------------------------------------------------------------------------

# don't import other moca modules from this file. (exclude moca_data)
from dotenv import load_dotenv
from setproctitle import setproctitle
from atexit import register
from os import environ
from sys import platform
from pathlib import Path
from ..moca_data.config import __PROCESS_NAME__, __DEBUG_MODE__

# -------------------------------------------------------------------------- Imports --

# -- Start Up --------------------------------------------------------------------------

# load startup file.
from ..moca_data import startup as _

# get version info
with open(
        str(Path(__file__).parent.joinpath('.version')),
        mode='r',
        encoding='utf-8'
) as __version_info:
    __version: str = __version_info.read()
del __version_info

# load environment variables.
load_dotenv(str(Path(__file__).parent.parent.joinpath('moca_data').joinpath('.env')))

# debug log
__debug_mode = __DEBUG_MODE__ if __DEBUG_MODE__ in (True, False) else True if str(environ.get('MOCA_DEBUG')) in (
    'y', 'Y', 'yes', 'Yes', 'YES', 'true', 'True', 'TRUE', 'T', 't', 'ok', 'Ok', 'OK', '1'
) else False
if __debug_mode:
    print(f'------ Moca Modules ({__version}) was loaded. ------')
del __version

# set process name.
if __PROCESS_NAME__ is not None:
    setproctitle(str(__PROCESS_NAME__))

# setup uvloop
if platform != 'win32' and platform != 'cygwin':
    try:
        from uvloop import install
        install()
        if __debug_mode:
            print(f'------ Setup uvloop successfully. ------')
    except (ImportError, ModuleNotFoundError):
        print(f'------ Setup uvloop failed. ------')
del __debug_mode


# run at exit
def exit_func():
    try:
        from . import atexit as _
    except (ImportError, ModuleNotFoundError):
        pass
    
    
register(exit_func)

# -------------------------------------------------------------------------- Start Up --
