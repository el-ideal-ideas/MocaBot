# -- Imports --------------------------------------------------------------------------

from typing import (
    Any, Tuple, Optional
)
from functools import partial
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import InvalidUsage
from datetime import datetime
from json import JSONDecodeError
try:
    from ujson import dumps, loads
except (ImportError, ModuleNotFoundError):
    from json import dumps as __dumps, loads

    # This is done in order to ensure that the JSON response is
    # kept consistent across both ujson and inbuilt json usage.
    dumps = partial(__dumps, separators=(",", ":"))
from ..moca_utils import try_to_bool, validate_argument
from ..moca_el_command import el_command_parser

# -------------------------------------------------------------------------- Imports --

# -- Private Functions --------------------------------------------------------------------------


def __get_param(json_data: dict, request: Request, key: str,
                type_: Any = None, default: Any = None, validate: Optional[dict] = None, from_: str = 'all') -> Any:
    for __key in key.split('|'):
        if from_ == 'all':
            data = json_data.get(
                __key,
                request.args.get(__key,
                                 request.form.get(__key,
                                                  request.headers.get(__key.upper().replace('_', '-'),
                                                                      request.files.get(__key,
                                                                                        request.cookies.get(__key)))))
            )
        elif from_ == 'json':
            data = json_data.get(__key)
        elif from_ == 'args':
            data = request.args.get(__key)
        elif from_ == 'form':
            data = request.form.get(__key)
        elif from_ == 'header':
            data = request.headers.get(__key.upper().replace('_', '-'))
        elif from_ == 'file':
            data = request.files.get(__key)
        elif from_ == 'cookie':
            data = request.cookies.get(__key)
        else:
            raise ValueError('form_ argument is only supported  (all, json, args, form, header, file)')
        if data is not None:
            break
    if type(data) is str:
        status, value = el_command_parser(data)
        if status:
            data = value
    if validate is not None and not validate_argument(data, **validate):
        return default
    if type_ is None or type_ is any:
        return data
    elif type(data) is type_:
        return data
    elif type(data) is str and type_ is int:  # str to int
        try:
            return int(data)
        except (ValueError, TypeError):
            return default
    elif (type(data) is int or type(data) is float) and type_ is str:  # int to str, float to str
        return str(data)
    elif type(data) is str and type_ is list:  # str to list
        try:
            data = loads(data)
            return data if type(data) is list else default
        except (ValueError, TypeError, JSONDecodeError):
            return default
    elif type(data) is str and type_ is dict:  # str to dict
        try:
            data = loads(data)
            return data if type(data) is dict else default
        except (ValueError, TypeError, JSONDecodeError):
            return default
    elif type(data) is str and type_ is bool:
        return try_to_bool(data)
    else:
        return default

# -------------------------------------------------------------------------- Private Functions --

# -- Utils --------------------------------------------------------------------------


def get_remote_address(request: Request) -> str:
    """Get remote address"""
    return request.remote_addr if request.remote_addr != '' else request.ip


def get_args(request: Request, *args, from_: str = 'all') -> Tuple:
    """
    Get arguments.
    if args is a string, use this value as the key.
    if args is a tuple and the length is more than 2,
    use args[0] as the key,  --  args[0] must be a string,
    use args[1] as the type info,  --  args[1] can be (int, float, bool, str, list, dict, tuple, etc...)
    use args[2] as the default value,  --  args[2] can be any value,
    use args[3] as a validate info.  --  args[3] must be a dict.The value will be passed to validate_argument function.
                                         for example:
                                         {
                                            'min_length': 8,
                                            'max_length': 32,
                                         }
    The value of from_ argument can be (all, json, args, form, header, file, cookie)
    """
    try:
        json_data = request.json if isinstance(request.json, dict) else {}
    except InvalidUsage:
        json_data = {}
    return tuple([__get_param(json_data, request, key, from_=from_) if isinstance(key, str) else
                  __get_param(json_data, request, key[0], key[1], from_=from_) if len(key) == 2 else
                  __get_param(json_data, request, key[0], key[1], key[2], from_=from_) if len(key) == 3 else
                  __get_param(json_data, request, key[0], key[1], key[2], key[3], from_=from_) for key in args])


def write_cookie(
        response: HTTPResponse,
        key: str,
        value: Any,
        expires: Optional[datetime] = None,
        path: Optional[str] = None,
        comment: Optional[str] = None,
        domain: Optional[str] = None,
        max_age: Optional[int] = None,
        secure: Optional[bool] = None,
        httponly: Optional[bool] = None,
) -> HTTPResponse:
    """
    Write a cookie
    :param response: the response object of sanic server.
    :param key: the key of cookie.
    :param value: the value of cookie (will be dumped as a json string).
    :param expires: The time for the cookie to expire on the client’s browser.
    :param path: The subset of URLs to which this cookie applies. Defaults to /.
    :param comment: A comment (metadata).
    :param domain: Specifies the domain for which the cookie is valid.
                   An explicitly specified domain must always start with a dot.
    :param max_age: Number of seconds the cookie should live for.
    :param secure: Specifies whether the cookie will only be sent via HTTPS.
    :param httponly: Specifies whether the cookie cannot be read by Javascript.
    :return: the response object of sanic server.
    """
    response.cookies[key] = dumps(value)
    if expires is not None:
        response.cookies[key]['expires'] = expires
    if path is not None:
        response.cookies[key]['path'] = path
    if comment is not None:
        response.cookies[key]['comment'] = comment
    if domain is not None:
        response.cookies[key]['domain'] = domain
    if max_age is not None:
        response.cookies[key]['max-age'] = max_age
    if secure is not None:
        response.cookies[key]['secure'] = secure
    if httponly is not None:
        response.cookies[key]['httponly'] = httponly
    return response

# -------------------------------------------------------------------------- Utils --
