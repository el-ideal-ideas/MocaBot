# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, List, Optional, Tuple, Callable, Any, Sequence, Dict, Iterable
)
from inspect import currentframe, types, stack
from traceback import format_exc, print_exc
from os.path import basename
from os import environ
from pathlib import Path
from sys import executable, argv, exit
from dotenv import load_dotenv
from subprocess import call
from git.repo.base import Repo
from random import randint
from time import time
from requests import get, Response, RequestException
from hashlib import md5, sha1, sha256, sha512, sha224, sha384
from datetime import datetime
from time import sleep
from threading import Thread
from aiohttp import ClientSession, ClientError
from io import StringIO
from aiofiles import open as aio_open
from uuid import uuid4
from re import compile
from gzip import compress, decompress
from multiprocessing import current_process
from pprint import pprint
from setproctitle import setproctitle
from functools import partial, wraps
from random import choice
from html import escape, unescape
from Crypto import Random
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from signal import signal, SIGTERM, SIG_DFL, SIG_IGN, SIGINT
from faker import Faker
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from prettytable import PrettyTable
from PIL import Image
from io import BytesIO
from shutil import copytree, rmtree, copy
from os import remove
try:
    from cloudpickle import dumps as p_dumps, loads as p_loads
except (ImportError, ModuleNotFoundError):
    from pickle import dumps as p_dumps, loads as p_loads
from json import JSONDecodeError
try:
    from ujson import dump as __dump, dumps as __dumps, loads
    dump = partial(__dump, ensure_ascii=False)
    dumps = partial(__dumps, ensure_ascii=False)
    is_ujson = lambda: True
except (ImportError, ModuleNotFoundError):
    from json import dump as __dump, dumps as __dumps, loads

    # This is done in order to ensure that the JSON response is
    # kept consistent across both ujson and inbuilt json usage.
    dump = partial(__dump, separators=(",", ":"), ensure_ascii=False)
    dumps = partial(__dumps, separators=(",", ":"), ensure_ascii=False)
    is_ujson = lambda: False
from ..moca_core import (
    LICENSE, NEW_LINE, tz, ConsoleColor, HIRAGANA, KATAKANA, PROCESS_ID, IS_WIN, DIGITS, ENCODING, TMP_DIR,
    IS_UNIX_LIKE, SELF_PATH
)

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

email_pattern = compile('^[0-9a-z_./?-]+@([0-9a-z-]+.)+[0-9a-z-]+$')

en_faker: Faker = Faker('en_US')
jp_faker: Faker = Faker('ja_JP')
zh_faker: Faker = Faker('zh_CN')

# -------------------------------------------------------------------------- Variables --

# -- Utils --------------------------------------------------------------------------


def location() -> Tuple[str, str, int]:
    """
    :return: filename, caller name, line number
    """
    frame: Optional[types.FrameType] = currentframe()
    if frame is None:
        return 'unknown', 'unknown', -1
    else:
        return basename(frame.f_back.f_back.f_code.co_filename), \
               frame.f_back.f_back.f_code.co_name, \
               frame.f_back.f_back.f_lineno


def caller_name() -> str:
    """Return caller name."""
    frame: Optional[types.FrameType] = currentframe()
    if frame is None:
        return 'unknown'
    else:
        return frame.f_back.f_back.f_code.co_name


def self_name() -> str:
    """Return self name."""
    try:
        return stack()[1][3]
    except IndexError:
        return 'unknown'


def print_debug(msg: str) -> None:
    print('[DEBUG] ' + msg)


def print_info(msg: str) -> None:
    print('\033[32m' + '[INFO] ' + msg + '\033[0m')


def print_warning(msg: str) -> None:
    print('\033[33m' + '[WARNING] ' + msg + '\033[0m')


def print_error(msg: str) -> None:
    print('\033[31m' + '[ERROR] ' + msg + '\033[0m')


def print_critical(msg: str) -> None:
    print('\033[31m' + '[CRITICAL] ' + msg + '\033[0m')


def print_license() -> None:
    """Print license to console."""
    print(LICENSE)


def save_license_to_file(filename: Union[str, Path]) -> None:
    """Save the license to the file."""
    with open(str(filename), 'w') as file:
        print(LICENSE, end=NEW_LINE, file=file)
        pass


def install_modules(module: Union[str, List[str]], output: bool = False) -> None:
    """Install a python module use pip."""
    if IS_WIN:
        call(
            f"{executable} -m pip install pip {module if isinstance(module, str) else ' '.join(module)}"
            f" --upgrade --no-cache-dir {'> nul' if not output else ''}",
            shell=True
        )
    else:
        call(
            f"{executable} -m pip install pip {module if isinstance(module, str) else ' '.join(module)}"
            f" --upgrade --no-cache-dir {'> /dev/null' if not output else ''}",
            shell=True
        )


def install_requirements_file(filename: Union[str, Path]) -> None:
    """Install a python module use pip."""
    if IS_WIN:
        call(f"{executable} -m pip install pip --upgrade --no-cache-dir > nul", shell=True)
        call(
            f"{executable} -m pip install -r {str(filename)}"
            f" --upgrade --no-cache-dir > nul",
            shell=True
        )
    else:
        call(f"{executable} -m pip install pip --upgrade --no-cache-dir > /dev/null", shell=True)
        call(
            f"{executable} -m pip install -r {str(filename)}"
            f" --upgrade --no-cache-dir > /dev/null",
            shell=True
        )


def git_clone(url: str, path: Union[Path, str]) -> None:
    """Clone a git repository."""
    Repo.clone_from(url, str(path))


def wget(url: str, filename: Union[Path, str], timeout: int = 5, **kwargs) -> bool:
    """
    Download a file from url.
    if the http status code is 200 return true.
    """
    try:
        res: Response = get(url, allow_redirects=True, timeout=timeout, **kwargs)
        if res.status_code == 200:
            with open(str(filename), mode='wb') as file:
                file.write(res.content)
            return True
        else:
            return False
    except RequestException:
        return False


async def aio_wget(url: str, filename: Union[Path, str], timeout: int = 5, **kwargs) -> bool:
    """
    Download a file from url.
    if the http status code is 200 return true.
    """
    try:
        async with ClientSession() as session:
            async with session.get(url, allow_redirects=True, timeout=timeout, **kwargs) as res:
                if res.status == 200:
                    async with aio_open(str(filename), mode='wb') as file:
                        await file.write(await res.read())
                    return True
                else:
                    return False
    except ClientError:
        return False


def get_text_from_url(url: str, timeout: int = 5, **kwargs) -> str:
    """Get text content from a URL."""
    res: Response = get(url, allow_redirects=True, timeout=timeout, **kwargs)
    if res.status_code == 200:
        return res.text
    else:
        return ''


async def aio_get_text_from_url(url: str, timeout: int = 5, **kwargs) -> str:
    """Get text content from a URL."""
    async with ClientSession() as session:
        async with session.get(url, allow_redirects=True, timeout=timeout, **kwargs) as res:
            if res.status == 200:
                return await res.text()
            else:
                return ''


def wcheck(url: str, timeout: int = 5, **kwargs) -> bool:
    """If the http status is 200 return true."""
    try:
        res: Response = get(url, allow_redirects=True, timeout=timeout, **kwargs)
        return res.status_code == 200
    except RequestException:
        return False


async def aio_wcheck(url: str, timeout: int = 5, **kwargs) -> bool:
    """If the http status is 200 return true."""
    try:
        async with ClientSession() as session:
            async with session.get(url, allow_redirects=True, timeout=timeout, **kwargs) as res:
                return res.status == 200
    except ClientError:
        return False


def wstatus(url: str, timeout: int = 5, **kwargs) -> int:
    """return the http status code."""
    try:
        res: Response = get(url, allow_redirects=True, timeout=timeout, **kwargs)
        return res.status_code
    except RequestException:
        return -1


async def aio_wstatus(url: str, timeout: int = 5, **kwargs) -> int:
    """return the http status code."""
    try:
        async with ClientSession() as session:
            async with session.get(url, allow_redirects=True, timeout=timeout, **kwargs) as res:
                return res.status
    except ClientError:
        return -1


def disk_speed(path: Union[str, Path]) -> Tuple[float, float]:
    """return read(MB/s), write(MB/s)"""
    if Path(path).is_dir():
        filename = Path(path).joinpath('tmp.data')
    else:
        filename = Path(path)
    cluster_size = 64 * 1024
    file_size = 1000 * 1024 * 1024

    def calculate_results(start: float, end: float):
        diff = end - start
        speed = file_size / diff / 1024 / 1024
        return round(speed, 2)

    current = 0
    data = ""
    for i in range(cluster_size):
        data += str(randint(0, 1))
    start_write = time()
    file = open(str(filename), "wb")
    while current <= file_size:
        file.write(data.encode())
        current += cluster_size
    file.close()
    end_write = time()
    current = 0
    start_read = time()
    file = open(str(filename), "rb")
    while current <= file_size:
        file.read(cluster_size)
        current += cluster_size
    file.close()
    end_read = time()
    res_read = calculate_results(start_read, end_read)
    res_write = calculate_results(start_write, end_write)
    try:
        filename.unlink()
    except FileNotFoundError:
        pass
    return res_read, res_write


def check_hash(filename: Union[str, Path], algorithm: str) -> str:
    """
    Return the hash as a string.
    :param filename: the path to the file.
    :param algorithm: (md5, sha1, sha224, sha256, sha384, sha512)
    :return: the hash of the target file.
    """
    if 'md5' == algorithm:
        hash_ = md5()
    elif 'sha224' == algorithm:
        hash_ = sha224()
    elif 'sha256' == algorithm:
        hash_ = sha256()
    elif 'sha384' == algorithm:
        hash_ = sha384()
    elif 'sha512' == algorithm:
        hash_ = sha512()
    else:
        hash_ = sha1()

    with open(str(filename), mode='rb') as f:
        while True:
            chunk = f.read(2048 * hash_.block_size)
            if len(chunk) == 0:
                break
            hash_.update(chunk)

    digest = hash_.hexdigest()
    return digest


def get_time_string(only_date: bool = False) -> str:
    """
    Return current time as string.
    example
        only_date == True
            '2019-11-08'
        only_date == False
            '2019-11-08 15:12:16.036244'
    :return: time string.
    """
    if only_date:
        return str(datetime.now(tz).date())
    else:
        return str(datetime.now(tz))


def print_with_color(msg: str,
                     color: str) -> None:
    """
    print message to console with color.
    :param msg: message.
    :param color: color, can use data type ConsoleColor.
    :return: None.
    """
    print(color + msg + ConsoleColor.END)


def add_extension(filename: Union[Path, str],
                  extension: str) -> str:
    """
    Adds an extension to filename.
    :param filename: original filename.
    :param extension: extension to add.
    """
    # set name
    name: str = str(filename)
    # set extension
    if extension.startswith('.'):
        ext = extension
    else:
        ext = '.' + extension
    if name.endswith(ext):  # check name
        return name
    else:
        return name + ext


def add_dot_jpg(filename: Union[Path, str]) -> str:
    """Adds a .jpg extension to filename."""
    return add_extension(filename, '.jpg')


def add_dot_jpeg(filename: Union[Path, str]) -> str:
    """Adds a .jpeg extension to filename."""
    return add_extension(filename, '.jpeg')


def add_dot_gif(filename: Union[Path, str]) -> str:
    """Adds a .gif extension to filename."""
    return add_extension(filename, '.gif')


def add_dot_txt(filename: Union[Path, str]) -> str:
    """Adds a .txt extension to filename."""
    return add_extension(filename, '.txt')


def add_dot_png(filename: Union[Path, str]) -> str:
    """Adds a .png extension to filename."""
    return add_extension(filename, '.png')


def add_dot_csv(filename: Union[Path, str]) -> str:
    """Adds a .csv extension to filename."""
    return add_extension(filename, '.csv')


def add_dot_rtf(filename: Union[Path, str]) -> str:
    """Adds a .rtf extension to filename."""
    return add_extension(filename, '.rtf')


def add_dot_pdf(filename: Union[Path, str]) -> str:
    """Adds a .pdf extension to filename."""
    return add_extension(filename, '.pdf')


def add_dot_md(filename: Union[Path, str]) -> str:
    """Adds a .md extension to filename."""
    return add_extension(filename, '.md')


def add_dot_log(filename: Union[Path, str]) -> str:
    """Adds a .log extension to filename."""
    return add_extension(filename, '.log')


def add_dot_json(filename: Union[Path, str]) -> str:
    """Adds a .json extension to filename."""
    return add_extension(filename, '.json')


def add_dot_py(filename: Union[Path, str]) -> str:
    """Adds a .jpeg extension to filename."""
    return add_extension(filename, '.py')


def add_dot_cache(filename: Union[Path, str]) -> str:
    """Adds a .jpeg extension to filename."""
    return add_extension(filename, '.cache')


def add_dot_pickle(filename: Union[Path, str]) -> str:
    """Adds a .pickle extension to filename."""
    return add_extension(filename, '.pickle')


def add_dot_js(filename: Union[Path, str]) -> str:
    """Adds a .js extension to filename."""
    return add_extension(filename, '.js')


def add_dot_css(filename: Union[Path, str]) -> str:
    """Adds a .css extension to filename."""
    return add_extension(filename, '.css')


def add_dot_html(filename: Union[Path, str]) -> str:
    """Adds a .html extension to filename."""
    return add_extension(filename, '.html')


def remove_extension(filename: Union[Path, str]) -> str:
    """Remove extension."""
    name = str(filename)
    index = name.rfind('.')
    if index == -1:
        return name
    else:
        return name[:index]


def set_interval(function: Callable,
                 interval: float,
                 count: Optional[int] = None,
                 other_thread: bool = True) -> None:
    """
    Run function (count) times with interval(seconds).
    :param function: target function.
    :param interval: run function interval.
    :param count: run limit. if this value is None, run function without limit.
    :param other_thread: run on other thread.
    :return: None.
    """
    def __inner_wrapper() -> None:
        remaining = count
        while True:
            if (remaining is None) or (remaining > 0):
                if isinstance(remaining, int):
                    remaining -= 1
                sleep(interval)
                function()
            else:
                break
    if other_thread:
        thread = Thread(target=__inner_wrapper, daemon=True)
        thread.start()
    else:
        __inner_wrapper()


def set_timeout(function: Callable,
                timeout: float,
                other_thread: bool = True) -> None:
    """
    Run function with timeout (seconds).
    :param function: target function.
    :param timeout: timeout (seconds).
    :param other_thread: run on other thread.
    :return: None.
    """
    set_interval(function, timeout, count=1, other_thread=other_thread)


def on_other_thread(func):
    """This is a decorator, can run function on other thread."""
    @wraps(func)
    def decorator(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    return decorator


def is_hiragana(text: str) -> bool:
    """Check is text made of hiragana"""
    for character in text:
        if character not in HIRAGANA:
            return False
    return True


def is_small_hiragana(text: str) -> bool:
    """Check is text made of small hiragana"""
    small_hiragana = HIRAGANA[46:55]
    for character in text:
        if character not in small_hiragana:
            return False
    return True


def is_katakana(text: str) -> bool:
    """Check is text made of katakana"""
    for character in text:
        if character not in KATAKANA:
            return False
    return True


def is_small_katakana(text: str) -> bool:
    """Check is text made of small katakana"""
    small_katakana = KATAKANA[46:55]
    for character in text:
        if character not in small_katakana:
            return False
    return True


def hiragana_to_katakana(hiragana: str,
                         hide_other: bool = False) -> str:
    """Convert hiragana characters to katakana characters"""
    if hide_other:
        return ''.join([KATAKANA[HIRAGANA.index(character)] if character in HIRAGANA else
                        character if character in KATAKANA else
                        '' for character in hiragana])
    else:
        return ''.join([KATAKANA[HIRAGANA.index(character)] if character in HIRAGANA else
                        character for character in hiragana])


def katakana_to_hiragana(katakana: str,
                         hide_other: bool = False) -> str:
    """Convert katakana characters to hiragana characters"""
    if hide_other:
        return ''.join([HIRAGANA[KATAKANA.index(character)] if character in KATAKANA else
                        character if character in HIRAGANA else
                        '' for character in katakana])
    else:
        return ''.join([HIRAGANA[KATAKANA.index(character)] if character in KATAKANA else
                        character for character in katakana])


def check_length(min_length: int,
                 max_length: int,
                 mode: str = 'and',
                 *args) -> bool:
    """
    check items length is between min_length and max_length
    :param min_length: minimum length
    :param max_length: maximum length
    :param mode: check mode, 'and': all items need clear length check, 'or': more than one item need clear length check
    :param args: items
    :return: status, [correct] or [incorrect]
    """
    if mode == 'and':
        for item in args:
            if not (min_length <= len(item) <= max_length):
                return False  # if found incorrect item, stop check-loop and return False
        return True  # if can't found incorrect item, return True
    else:
        for item in args:
            if min_length <= len(item) <= max_length:
                return True  # if found correct item, stop check-loop and return True
        return False  # if can't found correct item, return False


def dump_json_beautiful(data: Any,
                        file: Union[StringIO, Path, str]) -> None:
    """Dump json data to file with beautiful format."""
    if isinstance(file, StringIO):
        dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        if isinstance(file, Path):
            path = file
        else:
            path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(file), mode='w', encoding=ENCODING) as output_file:
            dump(data, output_file, ensure_ascii=False, indent=4, sort_keys=True)


def dumps_json_beautiful(data: Any) -> str:
    """Dump json data as string with beautiful format."""
    return dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def contains_upper(text: str) -> bool:
    """If text contains upper case characters, return True."""
    for character in text:
        if character.isupper():
            return True
    return False


def contains_lower(text: str) -> bool:
    """If text contains lower case characters, return True."""
    for character in text:
        if character.islower():
            return True
    return False


def contains_alpha(text: str) -> bool:
    """If text contains alphabet, return True."""
    for character in text:
        if character.isalpha():
            return True
    return False


def contains_digit(text: str) -> bool:
    """If text contains a digit, return True."""
    for character in text:
        if character.isdigit():
            return True
    return False


def contains_symbol(text: str, symbols: Optional[str] = None) -> bool:
    """If text contains a symbol in symbols, return True."""
    if symbols is None:
        for character in text:
            if character.isascii() and (not character.isalnum()):
                return True
        return False
    else:
        for character in text:
            if character in symbols:
                return True
        return False


def only_consist_of(target: Union[str, List[str]], characters: Union[str, List[str]],) -> bool:
    """If 'target' only contains of 'characters' return True"""
    for character in target:
        if character not in characters:
            return False
    return True


def to_hankaku(text: str) -> str:
    """半角変換"""
    return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).replace('　', ' ')


def to_zenkaku(text: str) -> str:
    """全角変換"""
    return text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})).replace(' ', '　')


def check_email_format(email: str) -> bool:
    return email_pattern.match(email) is not None


def moca_dumps(obj: Any) -> bytes:
    """serialize and compress."""
    data = p_dumps(obj)
    if len(data) > 1024:
        return b'moca' + compress(data)
    else:
        return data


def moca_dump(obj: Any, filename: Union[Path, str]) -> None:
    """serialize and compress."""
    with open(str(filename), mode='wb') as file:
        file.write(moca_dumps(obj))


async def moca_aio_dump(obj: Any, filename: Union[Path, str]) -> None:
    """serialize and compress."""
    async with aio_open(str(filename), mode='wb') as file:
        await file.write(moca_dumps(obj))


def moca_loads(data: Optional[bytes]) -> Any:
    """Load serialized object."""
    if data is None:
        return None
    elif data[:4] == b'moca':
        return p_loads(decompress(data[4:]))
    else:
        return p_loads(data)


def moca_load(filename: Union[Path, str]) -> Any:
    """Load serialized object."""
    with open(str(filename), mode='rb') as file:
        return moca_loads(file.read())


async def moca_aio_load(filename: Union[Path, str]) -> Any:
    """Load serialized object."""
    async with aio_open(str(filename), mode='rb') as file:
        return moca_loads(await file.read())


def print_only_in_main_process(*args, sep: str = ' ', end: str = NEW_LINE, file=None) -> None:
    """When this process is main process, print message."""
    if current_process().pid == PROCESS_ID:
        print(*args, sep=sep, end=end, file=file)
        pass


def set_process_name(name: str) -> None:
    """Set a name for this process."""
    setproctitle(name)


def html_escape(text: str) -> str:
    """Escape html"""
    return escape(text)


def html_unescape(text: str) -> str:
    """Unescape html"""
    return unescape(text)


def word_block(text: str, blocked_words: List[str], replace: str = '****') -> str:
    """Replace blocked words in text."""
    tmp_string: str = text
    for word in blocked_words:
        if word in tmp_string:
            tmp_string = tmp_string.replace(word, replace)
    return tmp_string


def get_random_string(length: int,
                      characters: Optional[Sequence] = None) -> str:
    """
    Create a random string by characters.
    If characters is None create random string use uuid4.
    """
    if characters is None:
        return ''.join([uuid4().hex for _ in range((length // 32) + 1)])[0:length]
    else:
        return ''.join([str(choice(characters)) for _ in range(length)])


def try_to_int(text: str) -> Union[str, int]:
    """If the text can be convert to int, return int(data)."""
    try:
        return int(text)
    except (ValueError, TypeError):
        return text


def try_to_float(text: str) -> Union[str, float]:
    """If the text can be convert to float, return float(data)."""
    try:
        return float(text)
    except (ValueError, TypeError):
        return text


def try_to_bool(text: str) -> Union[str, bool]:
    """If the text is means True or False, return a bool."""
    if text in ('y', 'Y', 'yes', 'Yes', 'YES', 'true', 'True', 'TRUE', 'T', 't', 'ok', 'Ok', 'OK', '1'):
        return True
    elif text in ('n', 'N', 'no', 'No', 'NO', 'false', 'False', 'FALSE', 'F', 'f', '0'):
        return False
    else:
        return text


def try_to_obj(text: str) -> Any:
    """If the text can be load as a json, return a loaded object."""
    try:
        obj = loads(text)
        return obj
    except (ValueError, JSONDecodeError):
        return text


def parser_str(text: str) -> Any:
    """
    If the text can be convert to int, return int(data).
    If the text can be convert to float, return float(data).
    If the text is means True or False, return a bool.
    If the text can be load as a json, return a loaded object.
    Else return text directly.
    """
    res: Any
    res = try_to_int(text)
    if not isinstance(res, str):
        return res
    res = try_to_float(text)
    if not isinstance(res, str):
        return res
    res = try_to_bool(text)
    if not isinstance(res, str):
        return res
    res = try_to_obj(text)
    if not isinstance(res, str):
        return res


def create_a_big_file(filename: Union[Path, str], gb: int = 1) -> None:
    """Create a big file."""
    size = gb * 1024 * 1024
    tmp = b'0' * 1024
    with open(str(filename), mode='wb') as file:
        for _ in range(size):
            file.write(tmp)


def create_a_big_text_file(filename: Union[Path, str], gb: int = 1) -> None:
    """Create a big text file with random string."""
    size = gb * 1024 * 1024
    with open(str(filename), mode='w', encoding=ENCODING) as file:
        for _ in range(size):
            file.write(get_random_string(1024))


def get_random_bytes(length: int) -> bytes:
    """Get random bytes."""
    return Random.get_random_bytes(length)


def get_random_string_by_digits(length: int) -> str:
    """Create a random string use digits."""
    return get_random_string(length, DIGITS)


def get_random_string_by_hiragana(length: int) -> str:
    """Create a random string use japanese hiragana."""
    return get_random_string(length, HIRAGANA)


def get_random_string_by_katakana(length: int) -> str:
    """Create a random string use japanese katakana."""
    return get_random_string(length, KATAKANA)


def get_random_string_by_kana(length: int) -> str:
    """Create a random string use japanese kana."""
    return get_random_string(length, KATAKANA + HIRAGANA)


def debugger(func):
    """
    This is a decorator,
    When the string `--debug` in the sys.argv
    or `MOCA_DEBUG=1` was set by the system environment variable,
    system will print debug info to console.
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        if '--debug' in argv or str(environ.get('MOCA_DEBUG')) == '1':
            print(f'++ MocaDebugger <{func.__name__}> ++++++++++++++++++++++++++++++++++')
            print(f'Args: {", ".join([str(arg) for arg in args])}')
            print(f'Kwargs: {", ".join([f"{key}={kwargs[key]}" for key in kwargs])}')
            print(f'Start: {get_time_string()}')
            try:
                start = time()
                value = func(*args, **kwargs)
                end = time()
                print(f'Return: {value}')
                print(f'End: {get_time_string()}')
                print(f'Spend: {end - start}')
                print(f'++++++++++++++++++++++++++++++++++ MocaDebugger ++')
                return value
            except Exception as e:
                print(f'Exception: {e}')
                print(f'End: {get_time_string()}')
                print(f'++++++++++++++++++++++++++++++++++ MocaDebugger ++')
                raise
        else:
            return func(*args, **kwargs)

    return decorator


def get_env(key: str, res_type: Any = any, default: Any = None) -> Any:
    """Get a value from system environment."""
    value = environ.get(key)
    if value is None:
        return default
    elif res_type is any:
        return value
    else:
        if isinstance(value, res_type):
            return value
        if res_type == int and isinstance(value, str):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        else:
            return default


def load_env(filename: Union[str, Path], encoding: str = ENCODING) -> None:
    """Load a dotenv file."""
    load_dotenv(str(filename), encoding=encoding)


def run_system(
        main: Callable,
        args: Optional[Tuple] = None,
        kwargs: Optional[Dict] = None,
        requirements: Optional[List[str]] = None,
        startup: Optional[Callable] = None,
        cleanup: Optional[Callable] = None,
        keyboard_interrupt: Optional[Callable] = None,
        sys_exit: Optional[Callable] = None,
        restart_when_error: bool = False,
        error_log: Optional[Union[str, Path]] = None
) -> None:
    """
    Run the system.
    :param main: the main function of the system.
    :param args: the arguments for the main function.
    :param kwargs: the keyword arguments for the main function.
    :param requirements: the requirements of this system.
                         When the ImportError or ModuleNotFoundError occurred,
                         system will try install the requirements use pip command, and try import module again.
    :param startup: this function will be called before the main function.
    :param cleanup: the function will be called when the process exits.
    :param keyboard_interrupt: this function will be called when the KeyboardInterrupt occurred.
    :param sys_exit: this function will be called when the SystemExit occurred.
    :param restart_when_error: when some error occurred, try restart the main function.
    :param error_log: when the unknown error occurred. try save the error log to this file.
    """
    def __run_main(args_, kwargs_):
        if args_ is not None and kwargs_ is not None:
            main(*args_, **kwargs_)
        elif args_ is not None:
            main(*args_)
        elif kwargs_ is not None:
            main(**kwargs_)
        else:
            main()

    try:
        # startup
        if startup is not None:
            startup()
        # main
        __run_main(args, kwargs)
        # add cleanup signal handler.
        if cleanup is not None:

            def sig_handler(signum, frame) -> None:
                cleanup()
                exit(1)

            signal(SIGTERM, sig_handler)
    except (ImportError, ModuleNotFoundError):
        if requirements is not None:
            install_modules(requirements)
        # try restart system.
        run_system(main, args, kwargs, requirements, startup, cleanup, keyboard_interrupt, sys_exit, restart_when_error)
    except KeyboardInterrupt:
        if keyboard_interrupt is not None:
            keyboard_interrupt()
    except SystemExit:
        if sys_exit is not None:
            sys_exit()
    except Exception as error:
        # if unknown error occurred and the `restart_when_error` is True. Try restart the system.
        print(f'Some unknown error occurred. Try restart. <Exception: {error}>')
        print_exc()
        if error_log is not None:
            try:
                with open(str(error_log), mode='w', encoding=ENCODING) as f:
                    f.write(format_exc())
            except Exception as e:
                print(f"Can't save the error log to file. <Exception: {e}>")
                print_exc()
        if restart_when_error:
            run_system(
                main, args, kwargs, requirements, startup, cleanup, keyboard_interrupt, sys_exit, restart_when_error
            )
    finally:
        # cleanup
        if cleanup is not None:
            signal(SIGTERM, SIG_IGN)
            signal(SIGINT, SIG_IGN)
            cleanup()
            signal(SIGTERM, SIG_DFL)
            signal(SIGINT, SIG_DFL)


def check_function_speed(func: Callable, *args, **kwargs) -> int:
    """Return the time to execute the function."""
    start = time()
    func(*args, **kwargs)
    return int((time() - start) * 1000)


def try_print(*args, flag: bool, sep: str = ' ', end: str = '\n', file=None) -> None:
    """Only print when the `flag` is true."""
    if flag:
        print(*args, sep=sep, end=end, file=file)
        pass


def try_pprint(obj: Any, flag: bool,
               stream=None, indent=1, width=80, depth=None, compact=False, sort_dicts=True) -> None:
    """Only print when the `flag` is true."""
    if flag:
        pprint(obj, stream=stream, indent=indent, width=width, depth=depth, compact=compact, sort_dicts=sort_dicts)


async def aio_call(cmd: str) -> Tuple[bytes, bytes]:
    """Run shell command use asyncio."""
    sp = await create_subprocess_exec(
        *cmd.split(), stdout=PIPE, stderr=PIPE
    )
    stdout, stderr = await sp.communicate()
    return stdout, stderr


def print_new_line() -> None:
    """Print new line on console."""
    print()


def range_ext(func: Callable, start: int = 0, stop: int = 1024, step: int = 1) -> map:
    """A shortcut."""
    return map(func, range(start, stop, step))


def loop(func: Callable, args: Sequence, kwargs: dict, cnt: int) -> None:
    """Execute the function `cnt` times."""
    for _ in range(cnt):
        func(*args, **kwargs)


def slice_by_keyword(text: str, start: str, stop: str) -> str:
    """get a slice by keyword."""
    return text[text.index(start) + len(start):text.index(stop)]


def print_json_beautiful(data: Any) -> None:
    """Print json data to console with highlight."""
    try:
        print(
            highlight(
                dumps(loads(data), indent=2) if isinstance(data, str) else dumps(data, indent=2),
                JsonLexer(),
                TerminalFormatter()
            )
        )
    except (JSONDecodeError, ValueError):
        raise ValueError('invalid argument.')


def all_ascii(value: Iterable) -> bool:
    """Check string items in the value, If all string item is ascii, return True"""
    for item in value:
        if isinstance(item, str) and not item.isascii():
            return False
    return True


def all_alpha(value: Iterable) -> bool:
    """Check string items in the value, If all string item is alphabet, return True"""
    for item in value:
        if isinstance(item, str) and not item.isalpha():
            return False
    return True


def all_numeric(value: Iterable) -> bool:
    """Check string items in the value, If all string item is numeric, return True"""
    for item in value:
        if isinstance(item, str) and not item.isdigit():
            return False
    return True


def all_alnum(value: Iterable) -> bool:
    """Check string items in the value, If all string item is ascii or numeric, return True"""
    for item in value:
        if isinstance(item, str) and not item.isalnum():
            return False
    return True


def have_ascii(value: Iterable) -> bool:
    """Check string items in the value, If any item is ascii, return True"""
    for item in value:
        if isinstance(item, str) and item.isascii():
            return True
    return False


def have_alpha(value: Iterable) -> bool:
    """Check string items in the value, If any string item is alphabet, return True"""
    for item in value:
        if isinstance(item, str) and item.isalpha():
            return True
    return False


def have_numeric(value: Iterable) -> bool:
    """Check string items in the value, If any string item is numeric, return True"""
    for item in value:
        if isinstance(item, str) and item.isdigit():
            return True
    return False


def have_alnum(value: Iterable) -> bool:
    """Check string items in the value, If any string item is ascii or numeric, return True"""
    for item in value:
        if isinstance(item, str) and item.isalnum():
            return True
    return False


def validate_argument(
        value: Any,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        gt: Optional[int] = None,
        ge: Optional[int] = None,
        lt: Optional[int] = None,
        le: Optional[int] = None,
        is_ascii: bool = False,
        is_alpha: bool = False,
        is_numeric: bool = False,
        is_alnum: bool = False,
        is_in: List[Any] = [],
        not_in: List[Any] = [],
        contains: List[Any] = [],
        invalid_str: List[Any] = [],
) -> bool:
    """
    Validate argument.
    :param value: the target value.
    :param min_length: this param can validate str, list, tuple.
    :param max_length: this param can validate str, list, tuple.
    :param gt: grater than, this param can validate int, float.
    :param ge: grater than or equal to, this param can validate int, float.
    :param lt: less than, this param can validate int, float.
    :param le: less than or equal to, this param can validate int, float.
    :param is_ascii: the value must be a ascii string. this param can validate str, list, tuple.
    :param is_alpha: the value must only contains alphabet. this param can validate str, list, tuple.
    :param is_numeric: the value must only contains digits. this param can validate str, list, tuple.
    :param is_alnum: the value must only contains alphabet or digits. this param can validate str, list, tuple.
    :param is_in: this param can validate str, list, tuple. The value must in this argument.
    :param not_in: this param can validate str, list, tuple. The value must not contains all item in this argument.
    :param contains: this param can validate str, list, tuple. The value must contains all item in this argument.
    :param invalid_str: this param can validate str, the value can't contains invalid str.
    :return: bool: the validation status.
    """
    if isinstance(value, str) or isinstance(value, list) or isinstance(value, tuple):
        if is_in:
            if isinstance(value, str) and value not in is_in:
                return False
            elif not isinstance(value, str):
                for item in value:
                    if item not in is_in:
                        return False
        if not_in:
            if isinstance(value, str) and value in not_in:
                return False
            elif not isinstance(value, str):
                for item in value:
                    if item in not_in:
                        return False
        if contains:
            for item in contains:
                if item not in value:
                    return False
        if invalid_str:
            for item in invalid_str:
                if item in value:
                    return False
        if min_length is not None and len(value) < min_length:
            return False
        elif max_length is not None and len(value) > max_length:
            return False
        elif isinstance(value, str) and is_ascii and not value.isascii():
            return False
        elif not isinstance(value, str) and is_ascii and not all_ascii(value):
            return False
        elif isinstance(value, str) and is_alpha and not value.isalpha():
            return False
        elif not isinstance(value, str) and is_alpha and not all_alpha(value):
            return False
        elif isinstance(value, str) and is_numeric and not value.isnumeric():
            return False
        elif not isinstance(value, str) and is_numeric and not all_numeric(value):
            return False
        elif isinstance(value, str) and is_alnum and not value.isalnum():
            return False
        elif not isinstance(value, str) and is_alnum and not all_alnum(value):
            return False
        else:
            return True
    elif isinstance(value, int) or isinstance(value, float):
        if gt is not None and value <= gt:
            return False
        elif ge is not None and value < ge:
            return False
        elif lt is not None and value >= lt:
            return False
        elif le is not None and value > le:
            return False
        else:
            return True
    else:
        return True


def is_file(filename: Union[Path, str]) -> bool:
    """If this path is a file, return True."""
    return Path(filename).is_file()


def is_dir(dir_path: Union[Path, str]) -> bool:
    """If this path is a directory, return True."""
    return Path(dir_path).is_dir()


def print_table(table: list) -> None:
    """Print a list data as table."""
    t = PrettyTable()
    t.field_names = table[0]
    for row in table[1:]:
        t.add_row(row)
    print(t.to_string)


def create_tor_deny_config_for_nginx() -> str:
    ip_info = get_text_from_url("https://check.torproject.org/torbulkexitlist")
    config = "\n".join([f"deny {item};" for item in ip_info.splitlines()])
    return config


def pm() -> None:
    print("--- もっちもっちにゃんにゃん！ ---")


def pl() -> None:
    print('----------------------------------------------------------------------------')


def resize_img(file: Union[bytes, str, Path], width: int, height: int, export_format: str) -> bytes:
    img = Image.open(BytesIO(file) if isinstance(file, bytes) else file)
    img_resize = img.resize((width, height))
    img_bytes = BytesIO()
    img_resize.save(img_bytes, export_format)
    return img_bytes.getvalue()


def get_my_public_ip_v4() -> str:
    try:
        res = get_text_from_url('https://inet-ip.info/ip')
        if len(res) <= 15:
            return res
    except RequestException:
        pass
    try:
        res = get_text_from_url('https://api.ipify.org/')
        if len(res) <= 15:
            return res
    except RequestException:
        pass
    try:
        res = get_text_from_url('http://checkip.dyndns.com/').split(':')[1].strip().rstrip('</body></html>\r\n')
        if len(res) <= 15:
            return res
    except RequestException:
        pass
    return ''


def get_my_public_ip_v6() -> str:
    try:
        res = get_text_from_url('https://ident.me')
        if len(res) >= 16:
            return res
    except RequestException:
        pass
    try:
        res = get_text_from_url('https://icanhazip.com')
        if len(res) >= 16:
            return res
    except RequestException:
        pass
    try:
        res = get_text_from_url('https://www.trackip.net/ip')
        if len(res) >= 16:
            return res
    except RequestException:
        pass
    return ''


def get_my_public_ip() -> str:
    res = get_my_public_ip_v4()
    if res != '':
        return res
    return get_my_public_ip_v6()


def update_use_github(
        project_dir: Union[Path, str], url: str, keep_list: List[Union[Path, str]] = [], map_dir: str = ''
) -> None:
    git_dir = Path(project_dir).joinpath(uuid4().hex)
    git_clone(url, str(git_dir))
    if map_dir != '':
        tmp_dir, git_dir = git_dir, git_dir.joinpath(map_dir)
    for keep in keep_list:
        from_ = Path(keep)
        to_ = git_dir
        tmp = []
        while from_ != Path(project_dir):
            tmp.append(from_.name)
            from_ = from_.parent
        from_ = Path(keep)
        for i in tmp:
            to_ = to_.joinpath(i)
        try:
            if IS_UNIX_LIKE:
                call(f'rm -rf {to_}', shell=True)
            else:
                to_.unlink(missing_ok=True)
            copy(str(from_), str(to_))
        except IsADirectoryError:
            try:
                rmtree(str(to_))
            except FileNotFoundError:
                pass
            copytree(str(from_), str(to_))
    copytree(str(git_dir), str(TMP_DIR.joinpath(git_dir.name)))
    rmtree(str(project_dir))
    copytree(str(TMP_DIR.joinpath(git_dir.name)), str(project_dir))
    rmtree(str(TMP_DIR.joinpath(git_dir.name)))


def update_moca_modules() -> None:
    update_use_github(
        SELF_PATH,
        'https://github.com/el-ideal-ideas/MocaModules',
        [
            SELF_PATH.joinpath('moca_data'),
            SELF_PATH.joinpath('moca_keep'),
        ],
        'moca_modules',
    )

# -------------------------------------------------------------------------- Utils --
