# -- Imports --------------------------------------------------------------------------

from pathlib import Path
from .. import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

# version
VERSION: str = mzk.get_str_from_file(Path(__file__).parent.joinpath('.version'))

# path
TOP_DIR: Path = Path(__file__).parent.parent.parent
CONFIG_DIR: Path = TOP_DIR.joinpath('configs')
LOG_DIR: Path = TOP_DIR.joinpath('logs')
SRC_DIR: Path = TOP_DIR.joinpath('src')
STORAGE_DIR: Path = TOP_DIR.joinpath('storage')

# create directories if not exists.
for __dir in [CONFIG_DIR, LOG_DIR, STORAGE_DIR]:
    __dir.mkdir(parents=True, exist_ok=True)
del __dir

# configs
SYSTEM_CONFIG: Path = CONFIG_DIR.joinpath('system.json')
SERVER_CONFIG: dict = mzk.load_json_from_file(CONFIG_DIR.joinpath('server.json'))
SANIC_CONFIG: dict = mzk.load_json_from_file(CONFIG_DIR.joinpath('sanic.json'))
DB_CONFIG: dict = mzk.load_json_from_file(CONFIG_DIR.joinpath('database.json'))
IP_BLACKLIST_FILE: Path = CONFIG_DIR.joinpath('ip_blacklist.json')
API_KEY_FILE: Path = CONFIG_DIR.joinpath('api_key.json')
FLAGS_FILE: Path = CONFIG_DIR.joinpath('flags.json')
system_config: mzk.MocaConfig = mzk.MocaConfig(SYSTEM_CONFIG, manual_reload=True)
ip_blacklist: mzk.MocaSynchronizedJSONListFile = mzk.MocaSynchronizedJSONListFile(
    IP_BLACKLIST_FILE, manual_reload=True, remove_duplicates=True,
)
api_key_config: mzk.MocaSynchronizedJSONListFile = mzk.MocaSynchronizedJSONListFile(
    API_KEY_FILE, manual_reload=True
)
flags: mzk.MocaSynchronizedJSONDictFile = mzk.MocaSynchronizedJSONDictFile(
    FLAGS_FILE, manual_reload=True
)

ADD_BOT_DATA_QUERY = mzk.get_str_from_file(Path(__file__).parent.joinpath('add_bot_data.sql')).replace(
    '[el]#moca_prefix#', DB_CONFIG['mysql']['prefix']
)
GET_BOT_DATA_QUERY = mzk.get_str_from_file(Path(__file__).parent.joinpath('get_bot_data.sql')).replace(
    '[el]#moca_prefix#', DB_CONFIG['mysql']['prefix']
)
GET_DICT_COUNT_QUERY = mzk.get_str_from_file(Path(__file__).parent.joinpath('get_dict_count.sql')).replace(
    '[el]#moca_prefix#', DB_CONFIG['mysql']['prefix']
)
GET_CHAT_LOGS_QUERY = mzk.get_str_from_file(Path(__file__).parent.joinpath('get_chat_logs.sql')).replace(
    '[el]#moca_prefix#', DB_CONFIG['mysql']['prefix']
)
INSERT_CHAT_LOG_QUERY = mzk.get_str_from_file(Path(__file__).parent.joinpath('insert_chat_log.sql')).replace(
    '[el]#moca_prefix#', DB_CONFIG['mysql']['prefix']
)
ADD_BOT_QUERY = mzk.get_str_from_file(Path(__file__).parent.joinpath('add_bot.sql')).replace(
    '[el]#moca_prefix#', DB_CONFIG['mysql']['prefix']
)
GET_BOTS_QUERY = mzk.get_str_from_file(Path(__file__).parent.joinpath('get_bots.sql')).replace(
    '[el]#moca_prefix#', DB_CONFIG['mysql']['prefix']
)

# -------------------------------------------------------------------------- Variables --
