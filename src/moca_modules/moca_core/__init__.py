# -- Imports --------------------------------------------------------------------------

from . import startup as _

from .moca_variables import (
    ENCODING, NEW_LINE, SELF_PATH, TMP_DIR, CPU_COUNT, HOST_NAME, HOST, PROCESS_ID, PROCESS_NAME,
    RANDOM_KEY, TIME_ZONE, tz, LICENSE, EL_S, HIRAGANA, KATAKANA, ALPHABET_UPPERCASE, ALPHABET_LOWERCASE,
    DIGITS, CHINESE_DIGITS_SIMPLE, CHINESE_DIGITS_COMPLEX, JAPANESE_DIGITS_HIRAGANA, JAPANESE_DIGITS_KATAKANA,
    OS, IS_MAC, IS_WIN, IS_LINUX, IS_UNIX_LIKE, SYSTEM_DATA_PATH, CHINESE_WORD_BLACKLIST, IS_RHEL, IS_RHEL8,
    IS_CENTOS, IS_CENTOS8, IS_RHEL_LIKE, KERNEL, JAPANESE_WORD_BLACKLIST, IS_DEBUG, VERSION, MOCA_NULL, MOCA_TRUE,
    MOCA_FALSE, SCRIPT_DIR_PATH
)
from .uvloop import is_uvloop, try_setup_uvloop
from ..moca_data.config import CONFIG
from .ConsoleColor import ConsoleColor
from . import something as st

# -------------------------------------------------------------------------- Imports --


"""
This module provides some core data for moca_modules.

Requirements
------------
uvloop
    Ultra fast asyncio event loop.
setproctitle
    A Python module to customize the process title
python-dotenv
    Reads the key-value pair from .env file and adds them to environment variable.
pytz
    pytz brings the Olson tz database into Python. This library allows accurate 
    and cross platform timezone calculations using Python 2.4 or higher. 
    It also solves the issue of ambiguous times at the end of daylight saving time,
    which you can read more about in the Python Library Reference (datetime.tzinfo)
tzlocal
    This Python module returns a tzinfo object with the local timezone information under Unix and Win-32.
    It requires pytz, and returns pytz tzinfo objects.
    This module attempts to fix a glaring hole in pytz, that there is no way to get the local timezone information,
    unless you know the zoneinfo name, and under several Linux distros that’s hard or impossible to figure out.
    Also, with Windows different timezone system using pytz isn’t of much use unless 
    you separately configure the zoneinfo timezone name.
    With tzlocal you only need to call get_localzone() and you will get a tzinfo object with the local time zone info.
    On some Unices you will still not get to know what the timezone name is, but you don’t need that when you have
    the tzinfo file. However, if the timezone name is readily available it will be used.
"""
