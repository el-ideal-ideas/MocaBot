# -- Imports --------------------------------------------------------------------------

from sanic import Sanic, Blueprint
from threading import Thread
from limits.strategies import FixedWindowElasticExpiryRateLimiter
from limits.storage import MemoryStorage, RedisStorage
from copy import copy
from pymysql import MySQLError, IntegrityError
from .middlewares import middlewares
from .routes import blueprints
from .. import moca_modules as mzk
from .. import core

# -------------------------------------------------------------------------- Imports --

# -- App --------------------------------------------------------------------------

# Server header.
if 'server' not in map(lambda i: i.lower(), core.SERVER_CONFIG['headers'].keys()):
    core.SERVER_CONFIG['headers']['Server'] = f'MocaBot({core.VERSION})'
# Access-Control-Allow-Credentials header.
if core.SERVER_CONFIG['access_control_allowed_credentials']:
    core.SERVER_CONFIG['headers']['Access-Control-Allow-Credentials'] = True
else:
    pass
# Access-Control-Allow-Headers header.
if '*' in core.SERVER_CONFIG['access_control_allow_headers']:
    core.SERVER_CONFIG['headers']['Access-Control-Allow-Headers'] = '*'
else:
    core.SERVER_CONFIG['headers']['Access-Control-Allow-Headers'] = ', '.join(
        core.SERVER_CONFIG['access_control_allow_headers']
    )
# Access-Control-Allow-Methods header.
if '*' in core.SERVER_CONFIG['access_control_allowed_methods']:
    core.SERVER_CONFIG['headers']['Access-Control-Allow-Methods'] = '*'
else:
    core.SERVER_CONFIG['headers']['Access-Control-Allow-Methods'] = ', '.join(
        core.SERVER_CONFIG['access_control_allowed_methods']
    )
# Access-Control-Max-Age header.
core.SERVER_CONFIG['headers']['Access-Control-Allow-Methods'] = int(
    core.SERVER_CONFIG['access_control_max_age']
)
# Access-Control-Expose-Headers
if '*' in core.SERVER_CONFIG['access_control_expose_headers']:
    core.SERVER_CONFIG['headers']['Access-Control-Expose-Headers'] = '*'
else:
    core.SERVER_CONFIG['headers']['Access-Control-Expose-Headers'] = ', '.join(
        core.SERVER_CONFIG['access_control_expose_headers']
    )


# Sanic App
moca_sanic: mzk.MocaSanic = mzk.MocaSanic(
    f'MocaBot({core.VERSION})',
    app=None,
    host=core.SERVER_CONFIG['address']['host'],
    port=int(core.SERVER_CONFIG['address']['port']),
    unix=core.SERVER_CONFIG['address']['unix'],
    ssl=None,
    certfile=core.SERVER_CONFIG['ssl']['cert'],
    keyfile=core.SERVER_CONFIG['ssl']['key'],
    log_dir=core.LOG_DIR,
    internal_key=None,
    access_log=core.SERVER_CONFIG['access_log'],
    log_level=core.SERVER_CONFIG['log_level'],
    use_ipv6=core.SERVER_CONFIG['address']['use_ipv6'],
    workers=core.SERVER_CONFIG['workers'],
    headers=core.SERVER_CONFIG['headers'],
    debug=core.SERVER_CONFIG['debug'],
    auto_reload=core.SERVER_CONFIG['auto_reload'],
    websocket=True,
    backlog=core.SERVER_CONFIG['backlog'],
    origins=core.SERVER_CONFIG['access_control_allowed_origins'],
)

moca_sanic.load_sanic_server_configs(core.SANIC_CONFIG)
app: Sanic = moca_sanic.app


# set event listener
async def before_server_start(app_: Sanic, loop):
    mzk.set_process_name(f'{app_.name} --- listener {mzk.get_my_pid()}')
    mzk.print_info(f'Starting Sanic server. -- {mzk.get_my_pid()}')

    app_.system_config: mzk.MocaConfig = mzk.MocaConfig(
        core.SYSTEM_CONFIG, manual_reload=True
    )
    app_.ip_blacklist: mzk.MocaSynchronizedJSONListFile = mzk.MocaSynchronizedJSONListFile(
        core.IP_BLACKLIST_FILE, manual_reload=True, remove_duplicates=True,
    )
    app_.api_key_config: mzk.MocaSynchronizedJSONListFile = mzk.MocaSynchronizedJSONListFile(
        core.API_KEY_FILE, manual_reload=True
    )
    app_.flags = mzk.MocaSynchronizedJSONDictFile(
        core.FLAGS_FILE, manual_reload=True
    )

    app_.dict_cache = {}
    app_.secure_log = mzk.MocaFileLog(core.LOG_DIR.joinpath('secure.log'))
    app_.scheduler = mzk.MocaScheduler()
    if core.SERVER_CONFIG['rate_limiter_redis_storage'] is None:
        app_._storage_for_rate_limiter = MemoryStorage()
    else:
        app_._storage_for_rate_limiter = RedisStorage(core.SERVER_CONFIG['rate_limiter_redis_storage'])
    app_.rate_limiter = FixedWindowElasticExpiryRateLimiter(app_._storage_for_rate_limiter)
    try:
        app_.mysql = mzk.MocaMysql(
            core.DB_CONFIG['mysql']['host'],
            int(core.DB_CONFIG['mysql']['port']),
            core.DB_CONFIG['mysql']['user'],
            core.DB_CONFIG['mysql']['password'],
            core.DB_CONFIG['mysql']['database'],
            int(core.DB_CONFIG['mysql']['min_size']),
            int(core.DB_CONFIG['mysql']['max_size']),
        )
        app_.mysql.force_sync = mzk.try_to_bool(core.DB_CONFIG['mysql']['force_sync'])
    except KeyError as e:
        mzk.print_error(f'Mysql database configuration error. missing key: {e}')
        mzk.sys_exit(1)
    except MySQLError as e:
        mzk.print_error("Can't connect to MySQL database, Please check your database configuration.")
        mzk.print_error("And make sure your database is online.")
        mzk.print_error("You can use 'python3 moca.py test-mysql-con' to check your database.")
        mzk.print_error(f"<MySQLError: {e}>")
        mzk.sys_exit(1)

    def __reload_timer(application: Sanic) -> None:
        while True:
            mzk.sleep(1)
            application.system_config.reload_file()
            application.ip_blacklist.reload_file()
            application.api_key_config.reload_file()
            application.flags.reload_file()

    app_._timer_thread = Thread(target=__reload_timer, args=(app_,), daemon=True)
    app_._timer_thread.start()

    app_.bots = {}

    def reload_bot(the_updated_key, old_value, new_value, *args, **kwargs) -> None:
        application = kwargs['app']
        for bot_dir in core.STORAGE_DIR.iterdir():
            if bot_dir.is_dir():
                application.bots[bot_dir.name] = mzk.MocaBot(bot_dir.name, bot_dir)
        con = application.mysql.get_a_new_con()
        cursor = con.cursor()
        cursor.execute(core.GET_BOTS_QUERY)
        res = cursor.fetchall()
        con.close()
        application.dict_cache['id'] = {}
        application.dict_cache['name'] = {}
        for info in res:
            application.dict_cache['id'][info[0]] = info[1]
            application.dict_cache['name'][info[1]] = info[0]

    reload_bot(None, None, None, app=app_)

    app_.flags.set('moca_bot_reload', False)
    app_.flags.add_handler(
        'moca_bot_reload' + str(mzk.get_my_pid()), 'moca_bot_reload', reload_bot, kwargs={'app': app_}
    )


async def after_server_start(app_: Sanic, loop):
    mzk.print_info(f'Started Sanic server. -- {mzk.get_my_pid()}')

    # run scheduled tasks.
    def dos_detect():
        info = copy(app_.dict_cache.get('dos-detect'))
        app_.dict_cache['dos-detect'] = {}
        if info is None:
            return None
        for ip, count in info.items():
            if count > core.system_config.get_config('dos_detect', int, 5000):
                app_.ip_blacklist.append(ip)
                app_.secure_log.write_log(
                    f"Add {ip} to the blacklist. <dos_detection>",
                    mzk.LogLevel.WARNING
                )

    app_.scheduler.add_event_per_second('Dos-detect', dos_detect, 5)


async def before_server_stop(app_: Sanic, loop):
    mzk.print_info(f'Stopping Sanic server. -- {mzk.get_my_pid()}')


async def after_server_stop(app_: Sanic, loop):
    mzk.print_info(f'Stopped Sanic server. -- {mzk.get_my_pid()}')


moca_sanic.before_server_start = before_server_start
moca_sanic.after_server_start = after_server_start
moca_sanic.before_server_stop = before_server_stop
moca_sanic.after_server_stop = after_server_stop


# Middleware
for item in middlewares.values():
    moca_sanic.add_middleware(item[1], item[0])


# Blueprint
app.blueprint(Blueprint.group(*blueprints, url_prefix='/moca-bot'))


# -------------------------------------------------------------------------- App --
