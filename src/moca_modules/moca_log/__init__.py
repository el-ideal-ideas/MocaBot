# -- Imports --------------------------------------------------------------------------

from .LogLevel import LogLevel
from .MocaFileLog import MocaFileLog
from .MocaAsyncFileLog import MocaAsyncFileLog

# -------------------------------------------------------------------------- Imports --

"""
This is a simple logging module.
MocaFileLog can write logs in other thread, to return the response more quickly.
MocaAsyncFileLog can write logs use asyncio.

Requirements
------------
aiofiles
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
"""