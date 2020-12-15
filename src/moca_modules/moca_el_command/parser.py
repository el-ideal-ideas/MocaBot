# -- Imports --------------------------------------------------------------------------

from typing import (
    Tuple, Any
)
from datetime import datetime
from random import randint, randrange, random
from uuid import uuid4, uuid1
from multiprocessing import current_process
from os import cpu_count
from . import command as cmd
from ..moca_core import tz
from ..moca_utils import get_random_string, get_random_string_by_digits, get_random_bytes
from json import JSONDecodeError
try:
    from ujson import loads
except (ImportError, ModuleNotFoundError):
    from json import loads

# -------------------------------------------------------------------------- Imports --

# -- Parser --------------------------------------------------------------------------


def el_command_parser(command: str) -> Tuple[bool, Any]:
    """
    Parser el commands.
    :param command: target string.
    :return: (status, response)
             status: detected el-command, or not.
             response: el-command response, if can't detect el-command, the response will be None.
    """
    # validate
    if not isinstance(command, str) or not command.startswith('[el]'):
        return False, None

    # -- parser ------------------------

    # date time commands
    if command == cmd.NOW:
        return True, datetime.now(tz)
    elif command == cmd.NOW_STR:
        return True, str(datetime.now(tz))
    elif command == cmd.NOW_DATE:
        return True, datetime.now(tz).date()
    elif command == cmd.NOW_DATE_STR:
        return True, datetime.now(tz).date()

    # random commands
    elif command == cmd.RANDOM:
        return True, random()
    elif command.startswith('[el]#moca_random_string<') and command.endswith('>#'):
        try:
            return True, get_random_string(int(command[24:-2]))
        except (TypeError, ValueError):
            return False, None
    elif command == cmd.RANDOM_INTEGER:
        return True, randint(0, 9)
    elif command.startswith('[el]#moca_random_integer_list<') and command.endswith('>#'):
        try:
            return True, get_random_string_by_digits(int(command[30:-2])).split()
        except (TypeError, ValueError):
            return False, None
    elif command.startswith('[el]#moca_random_integer_str<') and command.endswith('>#'):
        try:
            return True, get_random_string_by_digits(int(command[29:-2]))
        except (TypeError, ValueError):
            return False, None
    elif command.startswith('[el]#moca_random_bytes<') and command.endswith('>#'):
        try:
            return True, get_random_bytes(int(command[23:-2]))
        except (TypeError, ValueError):
            return False, None
    elif command.startswith('[el]#moca_random_range<') and command.endswith('>#'):
        try:
            start, end = command[23:-2].split(',')
            return True, randrange(int(start), int(end))
        except (TypeError, ValueError):
            return False, None

    # uuid commands
    elif command == cmd.UUID1:
        return True, uuid1()
    elif command == cmd.UUID1_HEX:
        return True, uuid1().hex
    elif command == cmd.UUID1_STR:
        return True, str(uuid1())
    elif command == cmd.UUID4:
        return True, uuid4()
    elif command == cmd.UUID4_HEX:
        return True, uuid4().hex
    elif command == cmd.UUID4_STR:
        return True, str(uuid4())

    # system commands
    elif command == cmd.PROCESS_ID:
        try:
            return True, int(current_process().pid)
        except (ValueError, TypeError):
            return True, 0
    elif command == cmd.PROCESS_NAME:
        return True, current_process().name
    elif command == cmd.CPU_COUNT:
        return True, cpu_count()

    # json commands
    elif command.startswith('[el]#moca_json<') and command.endswith('>#'):
        try:
            return True, loads(command[15:-2])
        except (TypeError, ValueError, JSONDecodeError):
            return False, None

    # other commands
    elif command == cmd.MOCHI:
        return True, 'もっちもっちにゃんにゃん！'
    else:
        return False, None

# -------------------------------------------------------------------------- Parser --
