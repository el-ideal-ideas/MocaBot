# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional
)
import typer
from time import sleep
from shutil import copy
from subprocess import call
from pathlib import Path
from sys import executable
from ..moca_mysql import test_mysql_connection
from ..moca_redis import test_redis_connection
from ..moca_core import VERSION, ENCODING, IS_UNIX_LIKE, SELF_PATH, SCRIPT_DIR_PATH, TMP_DIR
from ..moca_utils import (
    install_modules, print_json_beautiful, add_moca_modules_to_system, get_random_string, disk_speed,
    create_tor_deny_config_for_nginx, get_my_public_ip_v6, get_my_public_ip_v4, update_moca_modules
)
from ..moca_file import (
    write_str_to_file
)
from ..moca_data.requirements import REQUIREMENTS

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

GREEN_TRUE: str = typer.style("True", fg=typer.colors.GREEN)
RED_FALSE: str = typer.style("False", fg=typer.colors.RED)

# -------------------------------------------------------------------------- Variables --

# -- Public Functions --------------------------------------------------------------------------


def green_msg(msg: str) -> str:
    return typer.style(msg, fg=typer.colors.GREEN)


def red_msg(msg: str) -> str:
    return typer.style(msg, fg=typer.colors.RED)


# -------------------------------------------------------------------------- Public Functions --

# -- Console --------------------------------------------------------------------------

typer_console: typer.Typer = typer.Typer()


@typer_console.command('hello', hidden=True)
def hello_world() -> None:
    """Print Hello World!"""
    print('Hello World!')


@typer_console.command('zen', hidden=True)
def zen() -> None:
    """Print python zen."""
    import this


@typer_console.command('say-mochimochi', hidden=True)
def mochimochi(loop: bool = False) -> None:
    """もっちもっちにゃんにゃん！"""
    if loop:
        while True:
            for i in 'もっちもっちにゃんにゃん！':
                print(i, end='', flush=True)
                sleep(0.1)
            print()
    else:
        typer.secho('もっちもっちにゃんにゃん！', fg=typer.colors.MAGENTA)


@typer_console.command('sanzijing', hidden=True)
def sanzijing() -> None:
    """打印三字经"""
    call(f'{executable} {str(SCRIPT_DIR_PATH.joinpath("sanzijing.py"))}', shell=True)


@typer_console.command('show-system-status')
def show_system_status() -> None:
    """Show system status."""
    call(f'{executable} {str(SCRIPT_DIR_PATH.joinpath("show_status.py"))}', shell=True)


@typer_console.command('moca-modules-version')
def show_moca_modules_version() -> None:
    """Show the version info of moca modules."""
    typer.secho(f'Moca Modules <{VERSION}>')


@typer_console.command('random-string')
def random_string(length: int = 64) -> None:
    """Generate a random string"""
    typer.secho(get_random_string(length))


@typer_console.command('generate-random-key')
def generate_random_key() -> None:
    """Generate a random key."""
    typer.secho(get_random_string(256))


@typer_console.command('remove-all-python-modules')
def remove_all_python_modules() -> None:
    """Remove all python modules that are installed by pip."""
    tmp_file = str(TMP_DIR.joinpath("pip-module-list.txt"))
    call(f'{executable} -m pip freeze > {tmp_file}', shell=True)
    call(f'{executable} -m pip uninstall -y -r {tmp_file}', shell=True)
    Path(tmp_file).unlink()


@typer_console.command('update-requirements-for-moca-modules')
def update_requirements_for_moca_modules() -> None:
    """Install and update requirements."""
    install_modules(REQUIREMENTS, True)


@typer_console.command('update-moca-modules')
def update_moca_modules_use_github() -> None:
    """Get latest version of MocaModules from github."""
    update_moca_modules()


@typer_console.command('add-moca-modules-to-my-system')
def add_moca_modules_to_my_system(key: str = '') -> None:
    """
    Copy moca_modules to /opt/python_modules/moca_modules or C:\\Program Files\\python_modules\\moca_modules
    """
    try:
        add_moca_modules_to_system(key)
        if IS_UNIX_LIKE:
            cli_path = '/usr/local/bin/moca-cli'
            if Path(cli_path).is_file():
                Path(cli_path).unlink()
            copy(str(SELF_PATH.joinpath('moca-cli')), cli_path)
            call(f'chmod +x {cli_path}', shell=True)
        typer.secho(green_msg('successfully.'))
    except PermissionError:
        typer.secho(red_msg('Permission denied: please run this command with root permission again.'))


@typer_console.command('test-mysql-con')
def test_mysql(host: str, port: int, username: str, password: str, dbname: str) -> None:
    """
    Test the connection of mysql server.
    """
    status, msg = test_mysql_connection(host, port, username, password, dbname)
    typer.secho('------------ Testing ------------')
    typer.secho(f'Host:\t\t {host}')
    typer.secho(f'Port:\t\t {port}')
    typer.secho(f'User:\t\t {username}')
    typer.secho(f'Pass:\t\t {password}')
    typer.secho(f'Connection:\t {GREEN_TRUE if status else RED_FALSE}')
    typer.secho(f'Message:\t {green_msg(msg) if status else red_msg(msg)}')
    typer.secho('------------ Tested ------------')


@typer_console.command('test-redis-con')
def test_redis(host: str, port: int, password: Optional[str] = None) -> None:
    """
    Test the connection of redis server.
    """
    status, msg = test_redis_connection(host, port, password)
    typer.secho('------------ Testing ------------')
    typer.secho(f'Host:\t\t {host}')
    typer.secho(f'Port:\t\t {port}')
    typer.secho(f'Pass:\t\t {password}')
    typer.secho(f'Connection:\t {GREEN_TRUE if status else RED_FALSE}')
    typer.secho(f'Message:\t {green_msg(msg) if status else red_msg(msg)}')
    typer.secho('------------ Tested ------------')


@typer_console.command('show-json')
def show_json(filename: str, encoding: str = ENCODING) -> None:
    """
    Print json data beautifully.
    """
    with open(filename, mode='r', encoding=encoding) as f:
        print_json_beautiful(f.read())


@typer_console.command('disk-speed')
def check_disk_speed(path: str) -> None:
    """Check disk speed."""
    read, write = disk_speed(path)
    typer.secho(f'Read Speed:\t {read} MB/s')
    typer.secho(f'Write Speed:\t {write} MB/s')


@typer_console.command('net-speed')
def check_network_speed() -> None:
    """Check the network speed."""
    call('speedtest-cli', shell=True)


@typer_console.command('create-tor-deny-config-file-for-nginx')
def create_tor_deny_config_file_for_nginx(filename: str) -> None:
    """Create tor deny config file for nginx server."""
    path = Path(filename)
    config = create_tor_deny_config_for_nginx()
    write_str_to_file(path, config)
    typer.secho(green_msg(f'Saved file to {path}.'))


@typer_console.command('my-public-ip')
def my_public_ip() -> None:
    v4 = get_my_public_ip_v4()
    v6 = get_my_public_ip_v6()
    if v4 != '':
        typer.secho(v4)
    if v6 != '':
        typer.secho(v6)

# -------------------------------------------------------------------------- Console --
