# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Dict
)
from pathlib import Path
from gzip import compress, decompress
from io import BytesIO, StringIO
from os import stat
from ..moca_core import ENCODING

# -------------------------------------------------------------------------- Imports --

# -- MocaFileCacheController --------------------------------------------------------------------------


class MocaFileCacheController:
    """
    This class can cache files in memory, to reduce disk IO.
    ファイルをメモリ内にキャッシュすることにより、IO負荷をへらす。
    把文件缓存到内存里面，缓解系统的IO负担。

    Attributes
    ----------
    self.compress_min_size: int
        If the file is larger than this size, It will compress.
    self._cache: Dict[str, bytes]
        The cache of files.
    self._timestamp: Dict[str, float]
        The timestamp of the cached files.
    """

    def __init__(
            self,
            compress_min_size: int = 1 * 1024 * 1024 * 8,  # 8MB
    ):
        """
        :param compress_min_size: If the file is larger than this size, It will compress.
        """
        self.compress_min_size: int = compress_min_size
        self._cache: Dict[str, bytes] = {}
        self._timestamp: Dict[str, float] = {}

    def _load(self, filename: str) -> bytes:
        """Cache the target file and return the content."""
        if filename in self._cache and self._timestamp[filename] == stat(str(filename)).st_mtime:
            if self._cache[filename].startswith(b'moca'):
                return decompress(self._cache[filename][4:])
            else:
                return self._cache[filename]
        else:
            with open(filename, mode='rb') as f:
                data = f.read()
                self._cache[filename] = data if len(data) < self.compress_min_size else b'moca' + compress(data)
                self._timestamp[filename] = stat(str(filename)).st_mtime
            return data

    def load_text_file(self, filename: Union[str, Path], encoding: str = ENCODING) -> StringIO:
        """Return the target file as a StringIO object."""
        return StringIO(self._load(str(filename)).decode(encoding))

    def load_raw_file(self, filename: Union[str, Path]) -> BytesIO:
        """Return the target file as a BytesIO object."""
        return BytesIO(self._load(str(filename)))

    def clear_cache(self, filename: Union[str, Path]) -> None:
        """Clear the cache of target file."""
        try:
            del self._cache[str(filename)]
            del self._timestamp[str(filename)]
        except KeyError:
            pass

    def clear_all_cache(self) -> None:
        """Clear all file cache."""
        self._cache = {}
        self._timestamp = {}

# -------------------------------------------------------------------------- MocaFileCacheController --
