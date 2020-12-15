# -- Imports --------------------------------------------------------------------------

from typing import (
    Any, Dict
)
from json import dumps as json_dumps, loads as json_loads
from ujson import dumps as ujson_dumps, loads as ujson_loads
from orjson import dumps as orjson_dumps, loads as orjson_loads
from simplejson import dumps as simplejson_dumps, loads as simplejson_loads
from rapidjson import dumps as rapidjson_dumps, loads as rapidjson_loads
from ..moca_utils import check_function_speed, try_print

# -------------------------------------------------------------------------- Imports --

# -- Private --------------------------------------------------------------------------


def __print(name: str, dump_speed: int, load_speed: int, output: bool) -> None:
    try_print(
        f"Name:\t\t {name},\t\t "
        f"dump_speed: {dump_speed} ms,\t\t "
        f"load_speed: {load_speed} ms.",
        flag=output
    )

# -------------------------------------------------------------------------- Private --

# -- JSON Test --------------------------------------------------------------------------


def json_test(obj: Any, output: bool = True) -> Dict[str, Dict[str, int]]:
    """
    Compare json modules.
    :param obj: a python object.
    :param output: if this value is True, print the results to console.
    :return: {'module_name': {'dump_speed': int, 'load_speed': int}}
    """
    res: Dict[str, Dict[str, int]] = {}
    json_string = json_dumps(obj)
    try_print('+++++++++++++++++++++++++++++++++++++++++++++++++++++', flag=output)
    for item in (
            ('json', json_dumps, json_loads),
            ('ujson', ujson_dumps, ujson_loads),
            ('orjson', orjson_dumps, orjson_loads),
            ('simplejson', simplejson_dumps, simplejson_loads),
            ('rapidjson', rapidjson_dumps, rapidjson_loads),
    ):
        res[item[0]] = {}
        res[item[0]]['dump_speed'] = check_function_speed(item[1], obj)
        res[item[0]]['load_speed'] = check_function_speed(item[2], json_string)
        __print(item[0], res[item[0]]['dump_speed'], res[item[0]]['load_speed'], output)
    try_print('+++++++++++++++++++++++++++++++++++++++++++++++++++++', flag=output)
    return res

# -------------------------------------------------------------------------- JSON Test --
from orjson import JSONDecodeError