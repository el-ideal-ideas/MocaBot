# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Optional, Any, List
)
from async_lru import alru_cache
from functools import lru_cache
from pathlib import Path
from aiofiles import open as aio_open
from os import stat, SEEK_END
try:
    from magic import from_file
    libmagic_flag = True
    # This module need libmagic.
    """
    CentOS
        dnf install file-devel
    Debian/Ubuntu
        sudo apt-get install libmagic1
    Windows
        pip install python-magic-bin
    macOS
        brew install libmagic
    """
except (ImportError, ModuleNotFoundError):
    from mimetypes import guess_type
    libmagic_flag = False
from json import JSONDecodeError
from functools import partial
try:
    from ujson import dumps as __dumps, loads

    dumps = partial(__dumps, indent=2, ensure_ascii=False)
except (ImportError, ModuleNotFoundError):
    from json import dumps as __dumps, loads

    # This is done in order to ensure that the JSON response is
    # kept consistent across both ujson and inbuilt json usage.
    dumps = partial(__dumps, indent=2, separators=(",", ":"), ensure_ascii=False)
from ..moca_core import ENCODING, NEW_LINE

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

MAXSIZE = 1024

# -------------------------------------------------------------------------- Variables --

# -- Utils --------------------------------------------------------------------------


def get_str_from_file(
        filename: Union[str, Path],
        encoding: str = ENCODING
) -> str:
    with open(str(filename), mode='r', encoding=encoding) as file:
        return file.read()


@lru_cache(maxsize=MAXSIZE)
def get_str_from_file_with_cache(
        filename: Union[str, Path],
        encoding: str = ENCODING
) -> str:
    return get_str_from_file(filename, encoding=encoding)


async def aio_get_str_from_file(
        filename: Union[str, Path],
        encoding: str = ENCODING
) -> str:
    async with aio_open(str(filename), mode='r', encoding=encoding) as file:
        return await file.read()


@alru_cache(maxsize=MAXSIZE)
async def aio_get_str_from_file_with_cache(
        filename: Union[str, Path],
        encoding: str = ENCODING
) -> str:
    return await aio_get_str_from_file(filename, encoding=encoding)


def get_bytes_from_file(filename: Union[str, Path]) -> bytes:
    with open(str(filename), mode='rb') as file:
        return file.read()


@lru_cache(maxsize=MAXSIZE)
def get_bytes_from_file_with_cache(filename: Union[str, Path]) -> bytes:
    return get_bytes_from_file(filename)


async def aio_get_bytes_from_file(filename: Union[str, Path]) -> bytes:
    async with aio_open(str(filename), mode='rb') as file:
        return await file.read()


@alru_cache(maxsize=MAXSIZE)
async def aio_get_bytes_from_file_with_cache(filename: Union[str, Path]) -> bytes:
    return await aio_get_bytes_from_file(filename)


def write_str_to_file(filename: Union[str, Path], text: str, encoding: str = ENCODING) -> None:
    with open(str(filename), mode='w', encoding=encoding) as file:
        file.write(text)


async def aio_write_str_to_file(filename: Union[str, Path], text: str, encoding: str = ENCODING) -> None:
    async with aio_open(str(filename), mode='w', encoding=encoding) as file:
        await file.write(text)


def write_bytes_to_file(filename: Union[str, Path], data: bytes) -> None:
    with open(str(filename), mode='wb') as file:
        file.write(data)


async def aio_write_bytes_to_file(filename: Union[str, Path], data: bytes) -> None:
    async with aio_open(str(filename), mode='wb') as file:
        await file.write(data)


def append_str_to_file(filename: Union[str, Path], text: str, encoding: str = ENCODING) -> None:
    with open(str(filename), mode='a', encoding=encoding) as file:
        file.write(text)


async def aio_append_str_to_file(filename: Union[str, Path], text: str, encoding: str = ENCODING) -> None:
    async with aio_open(str(filename), mode='a', encoding=encoding) as file:
        await file.write(text)


def get_mime_type(filename: Union[str, Path]) -> Optional[str]:
    if libmagic_flag:
        return from_file(str(filename), mime=True)
    else:
        return guess_type(str(filename))[0]


@lru_cache(maxsize=MAXSIZE)
def get_mime_type_with_cache(filename: Union[str, Path]) -> Optional[str]:
    return get_mime_type(filename)


def get_timestamp(filename: Union[str, Path]) -> float:
    return stat(str(filename)).st_mtime


def load_json_from_file(filename: Union[str, Path], encoding: str = ENCODING) -> Any:
    try:
        return loads(get_str_from_file(filename, encoding=encoding))
    except JSONDecodeError as e:
        raise ValueError(str(e))


@lru_cache(maxsize=MAXSIZE)
def load_json_from_file_with_cache(filename: Union[str, Path], encoding: str = ENCODING) -> Any:
    return load_json_from_file(filename, encoding=encoding)


async def aio_load_json_from_file(filename: Union[str, Path], encoding: str = ENCODING) -> Any:
    try:
        return loads(await aio_get_str_from_file(filename, encoding=encoding))
    except JSONDecodeError as e:
        raise ValueError(str(e))


@alru_cache(maxsize=MAXSIZE)
async def aio_load_json_from_file_with_cache(filename: Union[str, Path], encoding: str = ENCODING) -> Any:
    return await aio_load_json_from_file(filename, encoding=encoding)


def dump_json_to_file(obj: Any, filename: Union[str, Path], encoding: str = ENCODING) -> None:
    write_str_to_file(filename, dumps(obj), encoding=encoding)


async def aio_dump_json_to_file(obj: Any, filename: Union[str, Path], encoding: str = ENCODING) -> None:
    await aio_write_str_to_file(filename, dumps(obj), encoding=encoding)


def get_last_line(file, number: int = 1, chunk_size: int = 1024, newline: bytes = b'\n'):
    """The file must be opened as binary mode"""
    end: List[bytes] = []
    index = 0
    count = 0
    if number < 1:
        raise ValueError('number parameter must be greater than 0.')
    while True:
        # We grab chunks from the end of the file towards the beginning until we get a new line
        try:
            file.seek(-index - chunk_size, SEEK_END)
        except OSError:
            return b''.join(end)
        chunk = file.read(chunk_size)
        end.insert(0, chunk)
        index += chunk_size
        count += chunk.count(newline)
        if count < number:
            continue
        else:
            return newline.join(b''.join(end).split(newline)[-number:])


def get_str_from_end_of_file(
        filename: Union[str, Path],
        number: int = 1,
        encoding: str = ENCODING,
        chunk_size: int = 1024,
        newline: bytes = NEW_LINE.encode()
) -> str:
    with open(str(filename), mode='rb') as file:
        data = get_last_line(file, number, chunk_size, newline)
        return data.decode(encoding)


# -------------------------------------------------------------------------- Utils --
