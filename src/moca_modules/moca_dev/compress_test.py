# -- Imports --------------------------------------------------------------------------

from typing import (
    Dict, Tuple
)
from gzip import compress as gzip_compress, decompress as gzip_decompress
from bz2 import compress as bz2_compress, decompress as bz2_decompress
from zlib import compress as zlib_compress, decompress as zlib_decompress
from brotli import compress as brotli_compress, decompress as brotli_decompress
from lzma import (
    compress as lzma_compress, decompress as lzma_decompress,
    FORMAT_XZ, CHECK_CRC64, CHECK_CRC32, CHECK_NONE, FORMAT_ALONE
)
from ..moca_utils import check_function_speed, try_print

# -------------------------------------------------------------------------- Imports --

# -- Private --------------------------------------------------------------------------


def __print(res: Dict[str, Tuple[int, int, int]], size: int, key: str, output: bool) -> None:
    try_print(
        f"{key}:\t\tsize: {round(res[key][0] / 1024 / 1024, 4)} MB,\t "
        f"percent: {round((res[key][0]/size)*100, 2)} %,\t "
        f"compress_speed: {res[key][1]} ms,\t "
        f"decompress_speed: {res[key][2]} ms.",
        flag=output
    )

# -------------------------------------------------------------------------- Private --

# -- Functions --------------------------------------------------------------------------


def compress_test(data: bytes, output: bool = True) -> Dict[str, Tuple[int, int, int]]:
    """
    Compare compress modules.
    :param data: the data to compress.
    :param output: if this value is True, print the results to console.
    :return: {'module name': (<size of the compressed data>, <time to compress>, <time to decompress>)}
    """
    res: Dict[str, Tuple[int, int, int]] = {}
    try_print('+++++++++++++++++++++++++++++++++++++++++++++++++++++', flag=output)
    size = len(data)
    try_print(f'Original size: {round(size/1024/1024), 4} MB', flag=output)
    # gzip
    for i in range(10):
        tmp = gzip_compress(data, compresslevel=i)
        key = f'gzip(compress level {i})'
        res[key] = (
            len(tmp),
            check_function_speed(gzip_compress, data, compresslevel=i),
            check_function_speed(gzip_decompress, tmp)
        )
        __print(res, size, key, output)
    # bz2
    for i in range(1, 10):
        tmp = bz2_compress(data, compresslevel=i)
        key = f'bz2(compress level {i})'
        res[key] = (
            len(tmp),
            check_function_speed(bz2_compress, data, compresslevel=i),
            check_function_speed(bz2_decompress, tmp)
        )
        __print(res, size, key, output)
    # zlib
    for i in range(10):
        tmp = zlib_compress(data, level=i)
        key = f'zlib(compress level {i})'
        res[key] = (
            len(tmp),
            check_function_speed(zlib_compress, data, level=i),
            check_function_speed(zlib_decompress, tmp)
        )
        __print(res, size, key, output)
    # lzma
    tmp = lzma_compress(data, FORMAT_XZ, CHECK_CRC64)
    res[f'lzma(XZ - CRC64)'] = (
        len(tmp),
        check_function_speed(lzma_compress, data, FORMAT_XZ, CHECK_CRC64),
        check_function_speed(lzma_decompress, tmp, format=FORMAT_XZ)
    )
    __print(res, size, f'lzma(XZ - CRC64)', output)
    tmp = lzma_compress(data, FORMAT_XZ, CHECK_CRC32)
    res[f'lzma(XZ - CRC32)'] = (
        len(tmp),
        check_function_speed(lzma_compress, data, FORMAT_XZ, CHECK_CRC32),
        check_function_speed(lzma_decompress, tmp, format=FORMAT_XZ)
    )
    __print(res, size, f'lzma(XZ - CRC32)', output)
    tmp = lzma_compress(data, FORMAT_XZ, CHECK_NONE)
    res[f'lzma(XZ - NONE)'] = (
        len(tmp),
        check_function_speed(lzma_compress, data, FORMAT_XZ, CHECK_NONE),
        check_function_speed(lzma_decompress, tmp, format=FORMAT_XZ)
    )
    __print(res, size, f'lzma(XZ - NONE)', output)
    tmp = lzma_compress(data, FORMAT_ALONE, CHECK_NONE)
    res[f'lzma(ALONE - NONE)'] = (
        len(tmp),
        check_function_speed(lzma_compress, data, FORMAT_ALONE, CHECK_NONE),
        check_function_speed(lzma_decompress, tmp, format=FORMAT_ALONE)
    )
    __print(res, size, f'lzma(ALONE - NONE)', output)
    # brotli
    tmp = brotli_compress(data)
    key = 'brotli'
    res[key] = (
        len(tmp),
        check_function_speed(brotli_compress, data),
        check_function_speed(brotli_decompress, tmp)
    )
    __print(res, size, key, output)
    try_print('+++++++++++++++++++++++++++++++++++++++++++++++++++++', flag=output)
    return res

# -------------------------------------------------------------------------- Functions --
