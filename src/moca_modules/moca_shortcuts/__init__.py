# -- Imports --------------------------------------------------------------------------

from .shortcuts import (
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

# -------------------------------------------------------------------------- Imports --

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