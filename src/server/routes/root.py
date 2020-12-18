# -- Imports --------------------------------------------------------------------------

from typing import (
    Tuple
)
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json as original_json, file
from orjson import dumps as orjson_dumps
from functools import partial
json = partial(original_json, dumps=orjson_dumps)
from sanic.exceptions import Forbidden, ServerError
from time import time
from pymysql import IntegrityError, MySQLError
from ... import moca_modules as mzk
from ... import core
from .utils import check_root_pass

# -------------------------------------------------------------------------- Imports --

# -- Private --------------------------------------------------------------------------

# -------------------------------------------------------------------------- Private --

# -- Blueprint --------------------------------------------------------------------------

root: Blueprint = Blueprint('root', None)


@root.route('/reload', {'GET', 'POST', 'OPTIONS'})
async def reload_moca_bot(request: Request) -> HTTPResponse:
    check_root_pass(request)
    request.app.flags.set('moca_bot_reload', not request.app.flags.get('moca_bot_reload'))
    return text('success.')


@root.route('/list', {'GET', 'POST', 'OPTIONS'})
async def get_bot_list(request: Request) -> HTTPResponse:
    return json(list(request.app.bots.keys()))


@root.route('/list-str', {'GET', 'POST', 'OPTIONS'})
async def get_bot_list(request: Request) -> HTTPResponse:
    return text(', '.join(list(request.app.bots.keys())))


@root.route('/bots', {'GET', 'POST', 'OPTIONS'})
async def bots(request: Request) -> HTTPResponse:
    check_root_pass(request)
    res = request.app.mysql.execute_aio(core.GET_BOTS_QUERY)
    return json(res)


@root.route('/create-bot', {'GET', 'POST', 'OPTIONS'})
async def create_bot(request: Request) -> HTTPResponse:
    check_root_pass(request)
    name, *_ = mzk.get_args(
        request,
        ('name|n', str, None, {'max_length': 32}),
    )
    if name is None:
        raise Forbidden('name parameter format error.')
    if core.STORAGE_DIR.joinpath(name).is_dir():
        raise Forbidden('name is already exists.')
    try:
        await request.app.mysql.execute_aio(
            core.ADD_BOT_QUERY,
            (name,),
            True
        )
    except IntegrityError:
        raise Forbidden('name is already exists.')
    core.STORAGE_DIR.joinpath(name).mkdir(parents=True, exist_ok=True)
    request.app.bots[name] = mzk.MocaBot(name, core.STORAGE_DIR.joinpath(name))
    request.app.flags.set('moca_bot_reload', not request.app.flags.get('moca_bot_reload'))
    return text('success.')


@root.route('/study', {'GET', 'POST', 'OPTIONS'})
async def study(request: Request) -> HTTPResponse:
    check_root_pass(request)
    name, message, message_list = mzk.get_args(
        request,
        ('name|n', str, None, {'max_length': 32}),
        ('message|msg|m', str, None, {'max_length': 512}),
        ('message_list|msg_list', list, None, {'max_length': 8192}),
    )
    if name is None:
        raise Forbidden('name parameter format error.')
    if message is None and message_list is None:
        raise Forbidden('message or message_list parameter format error.')
    bot = request.app.bots.get(name, None)
    bot_id = request.app.dict_cache['name'].get(name, 'unknown')
    if bot is None:
        raise Forbidden('Unknown bot name.')
    if message is not None:
        _ = bot.dialogue(message, study=True)
    else:
        for msg in message_list:
            if isinstance(msg, str) and len(msg) <= 512:
                _ = bot.dialogue(msg, study=True)
    bot.save()
    if message is not None:
        await request.app.mysql.execute_aio(
            core.ADD_BOT_DATA_QUERY,
            (bot_id, message),
            True
        )
    else:
        pool = await request.app.mysql.get_a_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cur:
                for msg in message_list:
                    if isinstance(msg, str) and len(msg) <= 512:
                        await cur.execute(core.ADD_BOT_DATA_QUERY, (bot_id, msg))
            await con.commit()
    request.app.flags.set('moca_bot_reload', not request.app.flags.get('moca_bot_reload'))
    return text('success.')


@root.route('/show-bot-dict', {'GET', 'POST', 'OPTIONS'})
async def show_bot_dict(request: Request) -> HTTPResponse:
    check_root_pass(request)
    name, *_ = mzk.get_args(
        request,
        ('name|n', str, None, {'max_length': 32}),
    )
    if name is None:
        raise Forbidden('name parameter format error.')
    bot_id = request.app.dict_cache['name'].get(name)
    if bot_id is None:
        raise Forbidden('unknown bot name.')
    res = request.app.mysql.execute_aio(core.GET_BOT_DATA_QUERY, (bot_id,))
    return json(res)


@root.route('/dialogue', {'GET', 'POST', 'OPTIONS'})
async def dialogue(request: Request) -> HTTPResponse:
    name, message, client_id = mzk.get_args(
        request,
        ('name|n', str, None, {'max_length': 32}),
        ('message|msg|m', str, None, {'max_length': 512}),
        ('client_id|id', str, None, {'max_length': 64})
    )
    if name is None:
        raise Forbidden('name parameter format error.')
    if message is None:
        raise Forbidden('message parameter format error.')
    bot = request.app.bots.get(name, None)
    bot_id = request.app.dict_cache['name'].get(name, 'unknown')
    if bot is None:
        raise Forbidden('Unknown bot name.')
    res_type, res_content = bot.dialogue(message)
    await request.app.mysql.execute_aio(
        core.INSERT_CHAT_LOG_QUERY,
        (mzk.get_remote_address(request), bot_id, message, res_content, res_type, client_id),
        True
    )
    return json({'res_type': res_type, 'res_content': res_content})


@root.route('/get-chat-logs', {'GET', 'POST', 'OPTIONS'})
async def get_chat_logs(request: Request) -> HTTPResponse:
    check_root_pass(request)
    name, *_ = mzk.get_args(
        request,
        ('name|n', str, None, {'max_length': 32}),
    )
    if name is None:
        raise Forbidden('name parameter format error.')
    bot_id = request.app.dict_cache['name'].get(name)
    if bot_id is None:
        raise Forbidden('unknown bot name.')
    res = request.app.mysql.execute_aio(core.GET_CHAT_LOGS_QUERY, (bot_id,))
    return json(res)

# -------------------------------------------------------------------------- Blueprint --
