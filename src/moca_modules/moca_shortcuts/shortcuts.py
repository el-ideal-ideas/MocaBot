# -- Imports --------------------------------------------------------------------------

# -------------------------------------------------------------------------- Imports --

# -- Shortcuts --------------------------------------------------------------------------

from time import sleep, time
from asyncio import sleep as aio_sleep, get_event_loop, get_event_loop_policy, get_running_loop, run
from os import _exit as os_exit
from sys import exit as sys_exit, argv, executable
from traceback import print_exc, format_exc
from pprint import pprint as pp
from timeit import timeit
from subprocess import call, check_output
try:
    from cloudpickle import dumps as p_dumps, loads as p_loads
except (ImportError, ModuleNotFoundError):
    from pickle import dumps as p_dumps, loads as p_loads
try:
    import cytoolz as toolz
except (ImportError, ModuleNotFoundError):
    import toolz
from json import dumps as json_dumps, loads as json_loads
from ujson import dumps as ujson_dumps, loads as ujson_loads
from orjson import dumps as orjson_dumps, loads as orjson_loads
from simplejson import dumps as simplejson_dumps, loads as simplejson_loads
from rapidjson import dumps as rapidjson_dumps, loads as rapidjson_loads
from functools import lru_cache
from async_lru import alru_cache
from random import choice, choices, sample, randint, uniform, getrandbits, shuffle
from uuid import uuid1, uuid4
import ulid
import shortuuid
from sys import getsizeof
from copy import copy
from async_timeout import timeout as aio_timeout
from timeout_decorator import timeout as timeout_decorator
from asyncio import TimeoutError as AsyncioTimeoutError
from timeout_decorator import TimeoutError as TimeoutDecoratorError
from retry_decorator import retry as retry_decorator
from datetime import datetime
from aiojobs import create_scheduler as create_aio_job_scheduler, Scheduler as AsyncJobScheduler
from janus import Queue as JanusQueue, PriorityQueue as JanusPriorityQueue, LifoQueue as JanusLifoQueue
from aiofiles import open as aio_open
import typer
from typer import style as tstyle, secho as tsecho, echo as techo, colors as tcolors


class MocaTimeoutError(AsyncioTimeoutError, TimeoutDecoratorError):
    """Timeout error for `aio_timeout` and `timeout_decorator`"""
    pass


# -------------------------------------------------------------------------- Shortcuts --
