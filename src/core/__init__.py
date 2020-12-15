# -- Imports --------------------------------------------------------------------------

from pathlib import Path
from warnings import catch_warnings, simplefilter
from .core import (
    VERSION, TOP_DIR, CONFIG_DIR, LOG_DIR, SRC_DIR, STORAGE_DIR, SYSTEM_CONFIG, SANIC_CONFIG, SERVER_CONFIG,
    IP_BLACKLIST_FILE, API_KEY_FILE, system_config, ip_blacklist, DB_CONFIG, FLAGS_FILE, flags, ADD_BOT_QUERY,
    ADD_BOT_DATA_QUERY, GET_BOT_DATA_QUERY, INSERT_CHAT_LOG_QUERY, GET_CHAT_LOGS_QUERY, GET_BOTS_QUERY
)
from .db import mysql, cursor
from .. import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

__bots_table = mzk.get_str_from_file(Path(__file__).parent.joinpath('bots_table.sql'))
__chat_logs_table = mzk.get_str_from_file(Path(__file__).parent.joinpath('chat_logs_table.sql'))
__bot_dict_table = mzk.get_str_from_file(Path(__file__).parent.joinpath('bot_dict_table.sql'))
with catch_warnings():
    simplefilter("ignore")
    cursor.execute(__bots_table % (DB_CONFIG['mysql']['prefix'],))
    mysql.commit()
    cursor.execute(__chat_logs_table % (DB_CONFIG['mysql']['prefix'], DB_CONFIG['mysql']['prefix']))
    mysql.commit()
    cursor.execute(__bot_dict_table % (DB_CONFIG['mysql']['prefix'], DB_CONFIG['mysql']['prefix']))
    mysql.commit()
del __bots_table, __chat_logs_table, __bot_dict_table

# -------------------------------------------------------------------------- Init --
