# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Tuple, List, Optional, Callable, Set
)
from pathlib import Path
from sanic import Sanic, Blueprint, __version__
from sanic.request import Request
from sanic.server import HttpProtocol
from sanic.log import logger, LOGGING_CONFIG_DEFAULTS
from sanic.exceptions import Forbidden, InvalidUsage, SanicException
from sanic.websocket import WebSocketProtocol
from sanic.response import HTTPResponse, text
from logging import INFO
from copy import copy
from ssl import SSLContext, Purpose, create_default_context
from pprint import pprint
from os import unlink
from socket import AF_INET6, SOCK_STREAM, socket, AF_UNIX
from multiprocessing import current_process
from datetime import datetime
from time import time
from spf import SanicPluginsFramework, SanicPlugin
from ..moca_core import LICENSE, IS_DEBUG, CPU_COUNT, tz, ENCODING, is_uvloop
from ..moca_utils import print_warning, print_info, get_random_string, print_error, is_file, set_process_name, is_ujson
from ..moca_file import load_json_from_file
from .utils import get_args

# -------------------------------------------------------------------------- Imports --

# -- MocaSanic --------------------------------------------------------------------------


class MocaSanic:
    """
    Sanic: Async Python 3.6+ web server/framework | Build fast. Run fast. https://sanicframework.org/

    Attributes
    ----------
    self._name: str
        the name of this server.
    self._app: Sanic
        the sanic application
    self._spf: Optional[SanicPluginsFramework]
        the sanic plugins framework.
    self._host: Optional[str]
        the host address.
    self._port: Optional[int]
        the port number.
    self._unix: Optional[str]
        use unix socket.
    self._ssl: Optional[SSLContext]
        ssl context for this server.
    self._certfile: Optional[Union[str, Path]]
        the path to ssl certificate file.
    self._keyfile: Optional[Union[str, Path]]
        the path to ssl key file.
    self._log_config: Optional[dict]
        the log configs
    self._internal_key: Optional[str]
        the internal key
    self._access_log: bool
        the access log flag.
    self._log_level: int
        the log level of sanic server.
    self._ipv6: bool
        the ipv6 flag.
    self._workers: int
        the workers number.
    self._headers: dict
        the response headers.
    self._debug: bool
        run sanic server in debug mode.
    self._auto_reload: Optional[bool]
        auto reload system when some changes are detected.
    self._websocket: bool
        if this flag is True, MocaSanic will use websocket protocol.
    self._backlog: int
        a number of unaccepted connections that the system will allow before refusing new connections.
    self._origins: List[str]
        the origins in this list, will be allowed.
    self._blueprint_list: List[Blueprint]
        all blueprint in this list will be added to the app.
    self._middleware_list: List[Tuple[str, Callable]]
        all middleware in this list will be added to the app.
    self._pid: Optional[int]
        the process id of the main process.
    self._running_lock: bool
        If sanic server is running, this flag will be set to True.
    self._env_prefix: str
        The prefix for the environment variables.
    """

    VERSION: str = '1.0.0'
    LICENSE: str = LICENSE

    SANIC_CONFIG_KEYS: Set[str] = {
        'REQUEST_MAX_SIZE', 'REQUEST_BUFFER_QUEUE_SIZE', 'REQUEST_TIMEOUT', 'RESPONSE_TIMEOUT', 'KEEP_ALIVE',
        'KEEP_ALIVE_TIMEOUT', 'WEBSOCKET_MAX_SIZE', 'WEBSOCKET_MAX_QUEUE', 'WEBSOCKET_READ_LIMIT',
        'WEBSOCKET_WRITE_LIMIT',
        'WEBSOCKET_PING_INTERVAL', 'WEBSOCKET_PING_TIMEOUT', 'GRACEFUL_SHUTDOWN_TIMEOUT', 'ACCESS_LOG',
        'FORWARDED_SECRET',
        'PROXIES_COUNT', 'FORWARDED_FOR_HEADER', 'REAL_IP_HEADER'
    }

    def __init__(
            self,
            name: str,
            app: Optional[Sanic] = None,
            host: Optional[str] = None,
            port: Optional[int] = None,
            unix: Optional[str] = None,
            ssl: Optional[SSLContext] = None,
            certfile: Optional[Union[str, Path]] = None,
            keyfile: Optional[Union[str, Path]] = None,
            log_dir: Optional[Union[str, Path]] = None,
            internal_key: Optional[str] = None,
            access_log: bool = False,
            log_level: int = INFO,
            use_ipv6: bool = False,
            workers: int = 0,
            headers: dict = {},
            debug: bool = IS_DEBUG,
            auto_reload: Optional[bool] = None,
            websocket: bool = False,
            backlog: int = 100,
            origins: List[str] = [],
    ):
        """
        :param name: the name of the sanic server.
        :param app: a instance of Sanic.
        :param host: the host address of the sanic server.
        :param port: the port of the sanic server.
        :param unix: use unix socket.
        :param ssl: the ssl context of the sanic server.
        :param certfile: the path to ssl certificate file.
        :param keyfile: the path to ssl key file.
        :param log_dir: the directory path of the logs.
        :param internal_key: the internal key. must be 1024 characters
        :param access_log: logging access.
        :param log_level: the log level of sanic server.
        :param use_ipv6: use ipv6
        :param workers: the number of workers,
                        if workers is less than 1, the workers number will be same to the number of cpu cores.
        :param headers: the response headers.
        :param debug: run sanic server in debug mode.
        :param auto_reload: auto reload system when some changes are detected.
        :param websocket: use websocket protocol.
        :param backlog: a number of unaccepted connections that the system
                        will allow before refusing new connections
        :param origins: the origins in this list, will be allowed.
        """
        # set name
        self._name: str = name
        # set host
        self._host: Optional[str] = host
        # set port
        self._port: Optional[int] = port
        # set unix socket
        self._unix: Optional[str] = unix
        # set ssl
        self._ssl: Optional[SSLContext] = ssl
        if (self._ssl is None) and (certfile is not None) and (keyfile is not None) and \
                is_file(certfile) and is_file(keyfile):
            self._ssl = self.create_ssl_context(certfile, keyfile)
        # set certification files
        self._certfile: Optional[Union[str, Path]] = certfile
        self._keyfile: Optional[Union[str, Path]] = keyfile
        # setup logging
        self._log_config: Optional[dict]
        if log_dir is not None:
            self._log_config = self._create_log_config(
                log_level,
                Path(log_dir) if isinstance(log_dir, str) else log_dir
            )
        else:
            self._log_config = None
        # set system environment prefix
        self._env_prefix: str = f'MOCA-{name.upper()}-'
        # set application
        self._app: Sanic = Sanic(
            name,
            log_config=self._log_config,
            load_env=self._env_prefix,
        ) if app is None else app
        # set plugin framework
        self._spf: Optional[SanicPluginsFramework] = None
        # set internal key
        self._internal_key: Optional[str] = internal_key
        # set access log flag
        self._access_log: bool = access_log
        # set log level
        self._log_level: int = log_level
        # set ipv6 flag
        self._ipv6: bool = use_ipv6
        # set workers number
        self._workers: int = workers if workers > 0 else CPU_COUNT
        # set headers
        self._headers: dict = headers
        # set debug flag
        self._debug: bool = debug
        # set reload flag
        self._auto_reload: Optional[bool] = auto_reload
        # set websocket flag
        self._websocket: bool = websocket
        # set backlog
        self._backlog: int = backlog
        # set origins
        self._origins: List[str] = origins
        # set blueprint list
        self._blueprint_list: List[Blueprint] = []
        # set middleware list
        self._middleware_list: List[Tuple[str, Callable]] = []
        # set pid
        self._pid: Optional[int] = current_process().pid
        # set running lock
        self._running_lock: bool = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def app(self) -> Sanic:
        return self._app

    @property
    def host(self) -> Optional[str]:
        return self._host

    @property
    def port(self) -> Optional[int]:
        return self._port

    @property
    def unix(self) -> Optional[str]:
        return self._unix

    @property
    def ssl(self) -> Optional[SSLContext]:
        return self._ssl

    @property
    def certfile(self) -> Optional[Union[str, Path]]:
        return self._certfile

    @property
    def keyfile(self) -> Optional[Union[str, Path]]:
        return self._keyfile

    @property
    def log_config(self) -> Optional[dict]:
        return self._log_config

    @property
    def internal_key(self) -> Optional[str]:
        return self._internal_key

    @property
    def access_log(self) -> bool:
        return self._access_log

    @property
    def log_level(self) -> int:
        return self._log_level

    @property
    def ipv6(self) -> bool:
        return self._ipv6

    @property
    def workers(self) -> int:
        return self._workers

    @property
    def headers(self) -> dict:
        return self._headers

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def auto_reload(self) -> Optional[bool]:
        return self._auto_reload

    @property
    def blueprint_list(self) -> List[Blueprint]:
        return self._blueprint_list

    @property
    def middleware_list(self) -> List[Tuple[str, Callable]]:
        return self._middleware_list

    @property
    def main_pid(self) -> Optional[int]:
        return self._pid

    @property
    def env_prefix(self) -> str:
        return self._env_prefix

    def _not_lock(self) -> bool:
        if not self._running_lock:
            return True
        else:
            print_warning(f'Sanic server is already running. If you want to change configs, Please stop the server.')
            return False

    def load_sanic_server_configs(
            self,
            config: Union[str, Path, dict],
            encoding: str = ENCODING,
            output: bool = True,
    ) -> bool:
        """Load the server configs."""
        sanic_config: dict
        if isinstance(config, str) or isinstance(config, Path):
            try:
                data = load_json_from_file(config, encoding)
            except (TypeError, ValueError) as decode_error:
                if output:
                    print_error(f'Some error occurred while decoding the config file. <{config}>')
                    print_error(f'JSONDecodeError, ValueError: {decode_error}')
                return False
            except FileNotFoundError as not_found_error:
                if output:
                    print_error(f"Can't found the config file. <{config}>")
                    print_error(f'FileNotFoundError: {not_found_error}')
                return False
            except PermissionError as permission_error:
                if output:
                    print_error(f"Can't open the config file. <{config}")
                    print_error(f"PermissionError: <{permission_error}")
                return False
            if isinstance(data, dict):
                sanic_config = data
            else:
                if output:
                    print_error(
                        'Loaded a invalid config file, the configs must be a dictionary format. <configs/sanic.json>')
                return False
        else:
            sanic_config = config
        for key in copy(list(sanic_config.keys())):
            if key not in self.SANIC_CONFIG_KEYS:
                del sanic_config[key]
                print_warning(
                    f"Found a unknown config key ({key}) in "
                    f"'{config if not isinstance(config, dict) else 'the argument'}'."
                    f" This config key will be ignored."
                )
        self._app.update_config(sanic_config)
        return True

    def add_response_header(self, key: str, value: str) -> None:
        """Add a response header."""
        if self._not_lock():
            self._headers[key] = value

    @staticmethod
    def _create_log_config(log_level, log_dir: Path) -> dict:
        """
        Create a logging configuration object for Sanic.
        """
        logger.setLevel(log_level)
        config: dict = copy(LOGGING_CONFIG_DEFAULTS)
        config['handlers']['root_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'generic',
            'filename': str(log_dir.joinpath('root.log'))
        }
        config['handlers']['error_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'generic',
            'filename': str(log_dir.joinpath('error.log'))
        }
        config['handlers']['access_file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'access',
            'filename': str(log_dir.joinpath('access.log'))
        }
        config['loggers']['sanic.root']['handlers'][0] = 'root_file'
        config['loggers']['sanic.error']['handlers'][0] = 'error_file'
        config['loggers']['sanic.access']['handlers'][0] = 'access_file'
        log_dir.mkdir(parents=True, exist_ok=True)
        return config

    @staticmethod
    def create_ssl_context(cert: Union[Path, str], key: Union[Path, str]) -> SSLContext:
        """Create a SSLContext."""
        ssl_context = create_default_context(Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=str(cert), keyfile=str(key))
        return ssl_context

    @staticmethod
    def generate_a_internal_key() -> str:
        """Create a random key file."""
        return get_random_string(1024)

    def _init_app(self) -> None:
        """Initialize the sanic application."""
        # ------ Version ------
        @self._app.route('/server-version', methods={'GET', 'POST', 'OPTIONS'})
        async def server_version(request: Request) -> HTTPResponse:
            return text(MocaSanic.VERSION)

        @self._app.route('/sanic-version', methods={'GET', 'POST', 'OPTIONS'})
        async def sanic_version(request: Request) -> HTTPResponse:
            return text(__version__)

        # ------ License ------
        @self._app.route('/server-license', methods={'GET', 'POST', 'OPTIONS'})
        async def show_license(request: Request) -> HTTPResponse:
            return text(MocaSanic.LICENSE)

        # ------ Mochi ------
        @self._app.route('/mochi', methods={'GET', 'POST', 'OPTIONS'})
        async def mochi(request: Request) -> HTTPResponse:
            return text('もっちもっちにゃんにゃん')

        # ------ 10086 ------
        @self._app.route('/10086', methods={'GET', 'POST', 'OPTIONS'})
        async def tushan(request: Request) -> HTTPResponse:
            return text('雁过拔毛，兽走留皮。')

        # ------ Ping ------
        @self._app.route('/ping', methods={'GET', 'POST', 'OPTIONS'})
        async def ping(request: Request) -> HTTPResponse:
            return text('success')

        # ------ DateTime ------
        @self._app.route('/datetime', methods={'GET', 'POST', 'OPTIONS'})
        async def date_time(request: Request) -> HTTPResponse:
            return text(str(datetime.now(tz=tz)))

        # ------ Epoch ------
        @self._app.route('/epoch', methods={'GET', 'POST', 'OPTIONS'})
        async def get_seconds_since_epoch(request: Request) -> HTTPResponse:
            return text(str(time()))

        # ------ Echo ------
        @self._app.route('/echo', methods={'GET', 'POST', 'OPTIONS'})
        async def echo(request: Request) -> HTTPResponse:
            message, *_ = get_args(
                request,
                ('message|m', str, 'invalid message', {'max_length': 1024, 'is_ascii': True})
            )
            return text(message)

        # ------ Status ------
        @self._app.route('/status', methods={'GET', 'POST', 'OPTIONS'})
        async def status(request: Request) -> HTTPResponse:
            return text(f'{self._name} is working...')

        # ------ Check Process ------
        @self._app.route('process')
        async def check_process(request: Request):
            return text(current_process().pid)

        # ------ Check origins ------
        if '*' in self._origins:
            @self._app.middleware('response')
            async def add_origin_header(request: Request, response: HTTPResponse):
                response.headers['Access-Control-Allow-Origin'] = '*'
        else:
            @self._app.middleware('response')
            async def add_origin_header(request: Request, response: HTTPResponse):
                origin = request.headers.get('origin')
                if origin is not None:
                    for item in self._origins:
                        if origin.startswith(item):
                            response.headers['Access-Control-Allow-Origin'] = origin

        @self._app.middleware('request')
        async def response_for_preflight(request: Request):
            if request.method.upper() == 'OPTIONS':
                return text('allowed.')

        # ------ Check internal key ------
        if self._internal_key != '' and self._internal_key is not None:
            @self._app.middleware('request')
            async def check_internal_key(request: Request):
                if request.headers.get('moca-internal-key') != self._internal_key:
                    raise Forbidden('Invalid internal key.')

        # ------ Set response headers ------
        @self._app.middleware('response')
        async def set_response_headers(request: Request, response: HTTPResponse):
            response.headers.update(self._headers)
            try:
                headers = request.ctx.response_header
                response.headers.update(headers)
            except AttributeError:
                pass

        # ------ Set debug middleware ------
        if self._debug:
            @self._app.middleware('request')
            async def before(request: Request):
                try:
                    json_data = request.json if isinstance(request.json, dict) else {}
                except InvalidUsage:
                    json_data = {}
                print()
                print('-- Receive a request -------------------------')
                print('-- url --')
                pprint(request.url)
                print('-- origin --')
                pprint(request.headers.get('origin'))
                print('-- method --')
                pprint(request.method)
                print('-- ip --')
                pprint(request.ip)
                print('-- json --')
                pprint(json_data)
                print('-- args --')
                pprint(request.args)
                print('-- form --')
                pprint(request.form)
                print('-- header --')
                pprint(request.headers)
                print('------------------------- Receive a request --')
                print()

            @self._app.exception(SanicException)
            async def sanic_exception(request: Request, exception):
                print('-- exception ----------------------------')
                print('-- url --')
                print(request.raw_url)
                print('-- exception --')
                print(exception)
                print('---------------------------- exception --')
                raise exception

        for blueprint in self._blueprint_list:
            self.app.blueprint(blueprint)

        for middleware_type, middleware in self._middleware_list:
            if isinstance(middleware, SanicPlugin):
                if self._spf is None:
                    self._spf = SanicPluginsFramework(self._app)
                self._spf.register_plugin(middleware)
            else:
                self._app.register_middleware(middleware, middleware_type)

        self._app.register_listener(self._before_server_start, 'before_server_start')
        self._app.register_listener(self._after_server_start, 'after_server_start')
        self._app.register_listener(self._before_server_stop, 'before_server_stop')
        self._app.register_listener(self._after_server_stop, 'after_server_stop')

    def add_blueprint(self, blueprint: Blueprint) -> None:
        """Add a blueprint."""
        if self._not_lock():
            self._blueprint_list.append(blueprint)

    def add_middleware(self, middleware: Callable, middleware_type: str) -> None:
        """Add a middleware"""
        if self._not_lock():
            self._middleware_list.append((middleware_type, middleware))

    def add_route(
            self,
            handler,
            uri,
            methods=frozenset({"GET"}),
            host=None,
            strict_slashes=None,
            version=None,
            name=None,
            stream=False,
    ):
        """Add a route"""
        self._app.add_route(handler, uri, methods, host, strict_slashes, version, name, stream)

    def static(self, uri: str, directory: Union[str, Path]) -> None:
        """Set a static directory for sanic server."""
        if self._not_lock():
            self._app.static(uri, str(directory))

    async def _before_server_start(self, app: Sanic, loop) -> None:
        await self.before_server_start(app, loop)

    async def _after_server_start(self, app: Sanic, loop) -> None:
        await self.after_server_start(app, loop)

    async def _before_server_stop(self, app: Sanic, loop) -> None:
        await self.before_server_stop(app, loop)

    async def _after_server_stop(self, app: Sanic, loop) -> None:
        await self.after_server_stop(app, loop)

    @staticmethod
    async def before_server_start(app: Sanic, loop):
        """Override this method to add listener."""
        pass

    @staticmethod
    async def after_server_start(app: Sanic, loop):
        """Override this method to add listener."""
        pass

    @staticmethod
    async def before_server_stop(app: Sanic, loop):
        """Override this method to add listener."""
        pass

    @staticmethod
    async def after_server_stop(app: Sanic, loop):
        """Override this method to add listener."""
        pass

    def run(self) -> None:
        """Run Sanic server."""
        set_process_name(f'{self._name} --- main process')
        self._init_app()
        try:
            print_info(f'uvloop: {is_uvloop()}, ujson: {is_ujson()}')
            if self._debug:
                print_info('Running MocaSanic module on debug mode.')
            if self._unix is not None:
                sock = socket(AF_UNIX, SOCK_STREAM)
                sock.bind(self._unix)
                print_info(f'MocaSanic bind to {self._unix}')
                self._app.run(
                    sock=sock,
                    access_log=self._access_log,
                    ssl=self._ssl,
                    debug=self._debug,
                    workers=self._workers,
                    protocol=HttpProtocol if not self._websocket else WebSocketProtocol,
                    auto_reload=self._auto_reload,
                    backlog=self._backlog
                )
            elif self._ipv6:
                print_info(f'MocaSanic Bind to {self._host}:{self._port}')
                sock = socket(AF_INET6, SOCK_STREAM)
                sock.bind((self._host, self._port))
                self._app.run(
                    sock=sock,
                    access_log=self._access_log,
                    ssl=self._ssl,
                    debug=self._debug,
                    workers=self._workers,
                    protocol=HttpProtocol if not self._websocket else WebSocketProtocol,
                    auto_reload=self._auto_reload,
                    backlog=self._backlog
                )
            else:
                print_info(f'MocaSanic Bind to {self._host}: {self._port}')
                self._app.run(
                    host=self._host,
                    port=self._port,
                    access_log=self._access_log,
                    ssl=self._ssl,
                    debug=self._debug,
                    workers=self._workers,
                    protocol=HttpProtocol if not self._websocket else WebSocketProtocol,
                    auto_reload=self._auto_reload,
                    backlog=self._backlog
                )
        except KeyboardInterrupt:
            print_info(f'Received KeyboardInterrupt, stopping sanic server...')
            raise
        except OSError as os_error:
            print_error(f'Sanic Http Server stopped. Please check your port is usable. <OSError: {os_error}>')
        except Exception as other_error:
            print_error(f'Sanic Http Server stopped, unknown error occurred. <Exception: {other_error}>')
        finally:
            if self._unix is not None:
                unlink(self._unix)
            elif self._ipv6:
                sock.close()

# -------------------------------------------------------------------------- MocaSanic --
