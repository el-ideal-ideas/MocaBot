"""
The modules developed for MocaSystem.
"""

"""
Important!
    moca_core module must on the top of this file. Because moca_core module contains start_up.py
    start_up.py must load at first.
"""

# -- Imports --------------------------------------------------------------------------

from .moca_data import config as __config

# -------------------------------------------------------------------------- Imports --

# -- moca_core --------------------------------------------------------------------------

from .moca_core import (
    ENCODING, NEW_LINE, SELF_PATH, TMP_DIR, CPU_COUNT, HOST_NAME, HOST, PROCESS_ID, PROCESS_NAME,
    RANDOM_KEY, TIME_ZONE, tz, LICENSE, EL_S, HIRAGANA, KATAKANA, ALPHABET_UPPERCASE, ALPHABET_LOWERCASE,
    DIGITS, CHINESE_DIGITS_SIMPLE, CHINESE_DIGITS_COMPLEX, JAPANESE_DIGITS_HIRAGANA, JAPANESE_DIGITS_KATAKANA,
    OS, IS_MAC, IS_WIN, IS_LINUX, IS_UNIX_LIKE, SYSTEM_DATA_PATH, CHINESE_WORD_BLACKLIST, IS_RHEL, IS_RHEL8,
    IS_CENTOS, IS_CENTOS8, IS_RHEL_LIKE, KERNEL, JAPANESE_WORD_BLACKLIST, is_uvloop, try_setup_uvloop, CONFIG, IS_DEBUG,
    VERSION, MOCA_NULL, MOCA_TRUE, MOCA_FALSE, SCRIPT_DIR_PATH
)
from .moca_core import ConsoleColor
from .moca_core import st

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

# -------------------------------------------------------------------------- moca_core --

# -- moca_file --------------------------------------------------------------------------

if __config.__LOAD_FILE__:
    from .moca_file import (
        MocaDirectoryCache, MocaFileAppendController, MocaFileCacheController, MocaSynchronizedBinaryFile,
        MocaSynchronizedJSONDictFile, MocaSynchronizedJSONFile, MocaSynchronizedJSONListFile, MocaSynchronizedTextFile,
        MocaWriteFileController, MocaWriteEncryptedFileController, get_str_from_file, get_str_from_file_with_cache,
        aio_get_str_from_file, aio_get_str_from_file_with_cache, get_mime_type, get_mime_type_with_cache, get_timestamp,
        get_bytes_from_file, get_bytes_from_file_with_cache,
        aio_get_bytes_from_file, aio_get_bytes_from_file_with_cache, write_str_to_file, aio_write_str_to_file,
        write_bytes_to_file, aio_write_bytes_to_file, append_str_to_file, aio_append_str_to_file, load_json_from_file,
        load_json_from_file_with_cache, aio_load_json_from_file, aio_load_json_from_file_with_cache,
        dump_json_to_file, aio_dump_json_to_file, get_last_line, get_str_from_end_of_file
    )

"""
This module provides some classes for manage files.

Requirements
------------
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
aiofiles        
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
async_lru
    Simple lru cache for asyncio
python-magic
    python-magic is a Python interface to the libmagic file type identification library.
    libmagic identifies file types by checking their headers according to a predefined list of file types.
    This module need libmagic.
    CentOS
        dnf install file-devel
    Debian/Ubuntu
        sudo apt-get install libmagic1
    Windows
        pip install python-magic-bin
    macOS
        brew install libmagic 
"""

# -------------------------------------------------------------------------- moca_file --

# -- moca_log --------------------------------------------------------------------------

if __config.__LOAD_LOG__:
    from .moca_log import (
        LogLevel, MocaFileLog, MocaAsyncFileLog
    )

"""
This is a simple logging module.
MocaFileLog can write logs in other thread, to return the response more quickly.
MocaAsyncFileLog can write logs use asyncio.

Requirements
------------
aiofiles
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
"""

# -------------------------------------------------------------------------- moca_log --

# -- moca_memory --------------------------------------------------------------------------

if __config.__LOAD_MEMORY__:
    from .moca_memory import MocaMemoryController

"""
This is the memory management module.

Requirements
------------
None
"""

# -------------------------------------------------------------------------- moca_memory --

# -- moca_redis --------------------------------------------------------------------------

if __config.__LOAD_REDIS__:
    from .moca_redis import MocaRedis, test_redis_connection

"""
This module is a redis client.

Requirements
------------
redis
    The Python interface to the Redis key-value store.
aioredis
    asyncio (PEP 3156) Redis client library.
"""

# -------------------------------------------------------------------------- moca_redis --

# -- moca_mysql --------------------------------------------------------------------------

if __config.__LOAD_MYSQL__:
    from .moca_mysql import MocaMysql, test_mysql_connection

"""
This is a mysql client module.

Requirements
------------
PyMySQL==0.9.2
    Pure Python MySQL Client
aiomysql
    aiomysql is a library for accessing a MySQL database from the asyncio
"""

# -------------------------------------------------------------------------- moca_mysql --

# -- moca_mail --------------------------------------------------------------------------

if __config.__LOAD_MAIL__:
    from .moca_mail import (
        send_mail, send_aio_mail, MocaMail
    )

"""
This is a simple mail client module.

Requirements
------------
aiosmtplib
    asyncio smtplib implementation.
"""

# -------------------------------------------------------------------------- moca_mail --

# -- moca_utils --------------------------------------------------------------------------

if __config.__LOAD_UTILS__:
    from .moca_utils import (
        location, caller_name, self_name, print_debug, print_info, print_warning, print_error, print_critical,
        print_license, save_license_to_file, install_modules, install_requirements_file, git_clone, wget, aio_wget,
        wcheck,
        aio_wget, wstatus, aio_wstatus, disk_speed, check_hash, get_time_string, print_with_color, add_extension,
        add_dot_jpg, add_dot_jpeg, add_dot_gif, add_dot_txt, add_dot_png, add_dot_csv, add_dot_rtf, add_dot_pdf,
        add_dot_md, add_dot_log, add_dot_json, add_dot_py, add_dot_cache, add_dot_pickle, add_dot_js, add_dot_css,
        add_dot_html, set_interval, set_timeout, on_other_thread, is_hiragana, is_katakana,
        is_small_hiragana, is_small_katakana, hiragana_to_katakana, katakana_to_hiragana, check_length,
        dump_json_beautiful,
        dumps_json_beautiful, contains_upper, contains_lower, contains_alpha, contains_digit, contains_symbol,
        only_consist_of, to_hankaku, to_zenkaku, check_email_format, moca_dumps, moca_dump, moca_aio_dump, moca_loads,
        moca_load, moca_aio_load, print_only_in_main_process, set_process_name, html_escape, html_unescape, word_block,
        get_random_string, try_to_int, create_a_big_file, get_random_bytes, get_random_string_by_digits,
        get_random_string_by_hiragana, get_random_string_by_katakana, get_random_string_by_kana, debugger,
        get_env, load_env, run_system, check_function_speed, try_print, try_pprint, aio_call, create_a_big_text_file,
        print_new_line, range_ext, loop, slice_by_keyword, print_json_beautiful, is_ujson, try_to_float, try_to_bool,
        try_to_obj, parser_str, en_faker, jp_faker, zh_faker, validate_argument, is_file, is_dir, get_text_from_url,
        aio_get_text_from_url, print_table, remove_extension, all_ascii, all_alnum, all_alpha, all_numeric,
        have_alnum, have_alpha, have_ascii, have_numeric, create_tor_deny_config_for_nginx, pm, pl, resize_img,
        get_my_public_ip, get_my_public_ip_v6, get_my_public_ip_v4, update_use_github, update_moca_modules
    )
    from .moca_utils import (  # The functions in this file, Only supports CentOS 8 and RHEL 8.
        get_centos_cpu_info, get_centos_cpu_model_name, get_centos_cpu_vendor_id, get_centos_cpu_cores,
        get_centos_cpu_cache_size, get_centos_cpu_mhz, get_centos_ssh_login_log, get_centos_accepted_ssh_login_log,
        get_centos_failed_ssh_login_log, get_centos_invalid_ssh_login_log, get_centos_accepted_ssh_login_count,
        get_centos_failed_ssh_login_count, get_centos_invalid_ssh_login_count, get_centos_recently_login_logs,
        get_centos_kernel,
    )
    from .moca_utils import (
        get_logical_cpu_count, get_cpu_count, get_cpu_percent, get_cpu_percent_per_cpu, get_total_memory,
        get_free_memory,
        get_used_memory, get_memory_percent, get_memory_info, get_total_swap_memory, get_free_swap_memory,
        get_used_swap_memory, get_swap_memory_percent, get_swap_memory_info, get_disk_usage, get_self_used_memory,
        get_self_used_memory_percent, get_my_username, is_root, get_my_pid, get_my_tid, add_moca_modules_to_system,
        is_main_process
    )

"""
This module provides many utilities.

Requirements
------------
GitPython
    GitPython is a python library used to interact with Git repositories
requests
    Requests is a simple, yet elegant HTTP library.
aiohttp
    Async http client/server framework
aiofiles
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
setproctitle
    A Python module to customize the process title
psutil
    Cross-platform lib for process and system monitoring in Python
pycryptodome
    PyCryptodome is a self-contained Python package of low-level cryptographic primitives.
python-dotenv
    Reads the key-value pair from .env file and adds them to environment variable.
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
cloudpickle
    Extended pickling support for Python objects
pygments
    Pygments is a generic syntax highlighter written in Python
Faker
    Faker is a Python package that generates fake data for you.
prettytable
    A simple Python library for easily displaying tabular data in a visually appealing ASCII table format
Pillow
    The friendly PIL fork (Python Imaging Library)
"""

# -------------------------------------------------------------------------- moca_utils --

# -- moca_word_filter --------------------------------------------------------------------------

if __config.__LOAD_WORD_FILTER__:
    from .moca_word_filter import (
        MocaSimpleWordFilter, MocaBSFilter, MocaDFAFilter
    )

"""
This is a word filter module.

Requirements
------------
None
"""

# -------------------------------------------------------------------------- moca_word_filter --

# -- moca_python --------------------------------------------------------------------------

if __config.__LOAD_PYTHON__:
    from .moca_python import MocaPy, exec_python_file, run_python_file

"""
This module can run python task on background process.

Requirements
------------
None

"""

# -------------------------------------------------------------------------- moca_python --

# -- moca_schedule --------------------------------------------------------------------------

if __config.__LOAD_SCHEDULE__:
    from .moca_schedule import MocaScheduler, schedule

"""
This is a simple scheduler module based on https://github.com/dbader/schedule

Requirements
------------
None
"""

# -------------------------------------------------------------------------- moca_schedule --

# -- moca_encrypt --------------------------------------------------------------------------

if __config.__LOAD_ENCRYPT__:
    from .moca_encrypt import (
        encrypt, decrypt, encrypt_string, decrypt_string, encrypt_file, decrypt_file,
        encrypt_file_aio, decrypt_file_aio, dumps_with_encryption, loads_with_encryption,
        dump_with_encryption, load_with_encryption, dump_with_encryption_aio,
        load_with_encryption_aio, MocaAES, MocaRSA, pyjs_encrypt, pyjs_decrypt
    )

"""
This is a encrypt and decrypt module.

Requirements
------------
aiofiles
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
pycryptodome
    PyCryptodome is a self-contained Python package of low-level cryptographic primitives.
cloudpickle
    Extended pickling support for Python objects
"""

# -------------------------------------------------------------------------- moca_encrypt --

# -- moca_shortcuts --------------------------------------------------------------------------

if __config.__LOAD_SHORTCUTS__:
    from .moca_shortcuts import (
        sleep, time, aio_sleep, os_exit, sys_exit, timeit, argv, executable,
        get_event_loop, get_event_loop_policy, get_running_loop, run,
        print_exc, format_exc,
        p_dumps, p_loads,
        json_dumps, json_loads,
        ujson_dumps, ujson_loads,
        simplejson_dumps, simplejson_loads,
        orjson_dumps, orjson_loads,
        rapidjson_dumps, rapidjson_loads,
        lru_cache, alru_cache,
        choice, choices, sample, randint, uniform, getrandbits, shuffle,
        uuid1, uuid4, ulid, shortuuid,
        getsizeof, aio_timeout, timeout_decorator, AsyncioTimeoutError, TimeoutDecoratorError, MocaTimeoutError,
        retry_decorator, datetime, pp,
        create_aio_job_scheduler, AsyncJobScheduler,
        JanusQueue, JanusPriorityQueue, JanusLifoQueue,
        aio_open, typer, techo, tsecho, tstyle, tcolors, toolz,
        call, check_output, copy
    )

"""
This module provides some shortcuts.

Requirements
------------
orjson
    Fast, correct Python JSON library supporting dataclasses, datetimes, and numpy
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
simplejson
    simplejson is a simple, fast, extensible JSON encoder/decoder for Python
python-rapidjson
    Python wrapper around rapidjson
cloudpickle
    Extended pickling support for Python objects
async_lru
    Simple lru cache for asyncio
ulid-py
    Universally Unique Lexicographically Sortable Identifier (ULID) in Python 3
shortuuid
    A generator library for concise, unambiguous and URL-safe UUIDs.
async-timeout
    asyncio-compatible timeout class
timeout-decorator
    Timeout decorator for Python
retry-decorator
    Decorator for retrying when exceptions occur
aiojobs
    Jobs scheduler for managing background task (asyncio)
janus
    Thread-safe asyncio-aware queue for Python
aiofiles        
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
typer
    Typer, build great CLIs. Easy to code. Based on Python type hints.
colorama
    Simple cross-platform colored terminal text in Python
toolz
    A functional standard library for Python.
cytoolz
    Cython implementation of Toolz: High performance functional utilities
"""

# -------------------------------------------------------------------------- moca_shortcuts --

# -- moca_counter --------------------------------------------------------------------------

if __config.__LOAD_COUNTER__:
    from .moca_counter import (
        AsyncInMemoryDriver, InMemoryDriver, AioRedisDriver, AsyncDriverInterface, DriverInterface, MocaCounter,
        SharedMemoryDriver, MocaAsyncCounter
    )

"""
This is a simple counter module.

Requirements
------------
aioredis
    asyncio (PEP 3156) Redis client library.
"""

# -------------------------------------------------------------------------- moca_counter --

# -- moca_share --------------------------------------------------------------------------

if __config.__LOAD_SHARE__:
    from .moca_share import (
        MocaMultiProcessLock, MocaSharedMemory
    )

"""
This module can share data between processes.

Requirements
------------
None
"""

# -------------------------------------------------------------------------- moca_share --

# -- moca_dev --------------------------------------------------------------------------

if __config.__LOAD_DEV__:
    from . import moca_dev as dev

"""
This module provides some functions for testing.

Requirements
------------
Benchmarker
    Benchmarker.py is an awesome benchmarking tool for Python.
orjson
    Fast, correct Python JSON library supporting dataclasses, datetimes, and numpy
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
simplejson
    simplejson is a simple, fast, extensible JSON encoder/decoder for Python
python-rapidjson
    Python wrapper around rapidjson
brotli
    Brotli compression format
sympy
    A computer algebra system written in pure Python
"""

# -------------------------------------------------------------------------- moca_dev --

# -- moca_cache --------------------------------------------------------------------------

if __config.__LOAD_CACHE__:
    from .moca_cache import MocaSimpleCache

"""
A simple in-memory cache.

Requirements
------------
cloudpickle
    Extended pickling support for Python objects
"""

# -------------------------------------------------------------------------- moca_cache --

# -- moca_el_command --------------------------------------------------------------------------

if __config.__LOAD_EL_PARSER__:
    from .moca_el_command import cmd, el_command_parser

"""
This module can parser el command.

Requirements
------------
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
"""

# -------------------------------------------------------------------------- moca_el_command --

# -- console --------------------------------------------------------------------------

if __config.__LOAD_CONSOLE__:
    from .moca_console import typer_console

"""
This module provides some console utility.

Requirements
------------
typer
    Typer, build great CLIs. Easy to code. Based on Python type hints.
colorama
    Simple cross-platform colored terminal text in Python
"""

# -------------------------------------------------------------------------- console --

# -- moca_config --------------------------------------------------------------------------

if __config.__LOAD_CONFIG__:
    from .moca_config import MocaConfig

"""
A json based config module.

Requirements
------------
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
"""

# -------------------------------------------------------------------------- moca_config --

# -- moca_sms --------------------------------------------------------------------------

if __config.__LOAD_SMS__:
    from .moca_sms import MocaTwilioSMS

"""
This module can send sms messages.

Requirements
------------
twilio
    https://jp.twilio.com/docs/sms
"""

# -------------------------------------------------------------------------- moca_sms --

# -- moca_leveldb --------------------------------------------------------------------------

if __config.__LOAD_LEVELDB__:
    from .moca_leveldb import MocaLevelDB

"""
This module is a wrapper of level DB.

Requirements
------------
plyvel
    Plyvel has a rich feature set, high performance, and a friendly Pythonic API.
    This module need leveldb.
"""

# -------------------------------------------------------------------------- moca_leveldb --

# -- moca_sanic --------------------------------------------------------------------------

if __config.__LOAD_SANIC__:
    from .moca_sanic import (
        MocaSanic, get_remote_address, get_args, write_cookie
    )

"""
This is a wrapper module for sanic.

Requirements
------------
sanic
    Async Python 3.6+ web server/framework | Build fast. Run fast.
sanic-plugins-framework
    Easily create Plugins for Sanic!
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
"""

# -------------------------------------------------------------------------- moca_sanic --

# -- moca_mmapq --------------------------------------------------------------------------

if __config.__LOAD_MMAPQ__:
    from .moca_mmapq import MocaMMAPQ

"""
This is a MMAP based queue implementation.
You can send data to another process, and receive data from another process.

Requirements
------------
cloudpickle
    Extended pickling support for Python objects
"""

# -------------------------------------------------------------------------- moca_mmapq --

# -- moca_twitter --------------------------------------------------------------------------

if __config.__LOAD_TWITTER__:
    from .moca_twitter import (
        MocaTwitter, TweepError, RateLimitError
    )

"""
This module can get data from twitter use twitter API.

Requirements
------------
tweepy
"""

# -------------------------------------------------------------------------- moca_twitter --

# -- moca_bot --------------------------------------------------------------------------

if __config.__LOAD_MOCA_BOT__:
    from .moca_bot import (
        tokenizer, analyze, MocaBot
    )

"""
日本語チャットボットモジュール

Requirements
------------
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
cloudpickle
    Extended pickling support for Python objects
janome
    Janome is a Japanese morphological analysis engine (or tokenizer, pos-tagger)
    written in pure Python including the built-in dictionary and the language model.
"""

# -------------------------------------------------------------------------- moca_bot --

# -- moca_keep --------------------------------------------------------------------------

from .moca_keep import *

# -------------------------------------------------------------------------- moca_keep --
