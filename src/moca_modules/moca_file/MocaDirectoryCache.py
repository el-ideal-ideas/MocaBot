# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Dict, Tuple, List, Optional
)
from pathlib import Path
from gzip import compress, decompress
from threading import Thread
from time import sleep
from .utils import get_mime_type, get_timestamp

# -------------------------------------------------------------------------- Imports --

# -- MocaDirectoryCache --------------------------------------------------------------------------


class MocaDirectoryCache:
    """
    This class can cache all files in the target directory, to reduce disk IO.
    指定ディレクトリ内のファイルをすべてメモリ上に保存し、ディスクIOを減らす。
    通过把指定文件夹内的所有文件缓存到内存来减少IO处理。

    Attributes
    ----------
    self._dir_path: Path
        The path ot the target directory.
    self._use_compress: bool
        Compress files in memory.
    self._cache: Dict[str, Tuple[Optional[str], bytes]]
        the cache of the files.
    self._timestamp: Dict[str, float]
        The timestamp of the files.
    """

    def __init__(
            self,
            dir_path: Union[str, Path],
            use_compress: bool = False,
            interval: float = 1.0,
            manual_reload: bool = False,
    ):
        """
        :param dir_path: The path ot the target directory.
        :param use_compress: Compress files in memory.
        :param interval: The interval (seconds) to refresh files.
        :param manual_reload: don't create the reload timer thread. You need run cache_files method manually.
        """
        # set parameters.
        self._dir_path: Path = Path(dir_path) if isinstance(dir_path, str) else dir_path
        self._use_compress: bool = use_compress
        self._cache: Dict[str, Tuple[Optional[str], bytes]] = {}
        self._timestamp: Dict[str, float] = {}
        # cache files.
        self.cache_files()

        # loop thread
        if not manual_reload:
            def __loop(self_: MocaDirectoryCache, interval_: float):
                while True:
                    sleep(interval_)
                    self_.cache_files()
            thread: Thread = Thread(target=__loop, args=(self, interval), daemon=True)
            thread.start()

    @property
    def dir_path(self) -> Path:
        return self._dir_path

    @property
    def cache(self) -> Dict[str, Tuple[Optional[str], bytes]]:
        return self._cache

    def cache_files(self) -> Dict[str, Tuple[Optional[str], bytes]]:
        """Load all files in the target directory in memory."""
        old_keys = set(self._cache.keys())
        new_keys = set([])
        path_list: List[Path] = [self._dir_path]
        while len(path_list) > 0:
            for item in path_list[0].iterdir():
                if item.is_dir():
                    path_list.append(item)
                else:
                    path = str(item)
                    timestamp = get_timestamp(path)
                    new_keys.add(path)
                    if self._timestamp.get(path) != timestamp:
                        with open(path, mode='rb') as f:
                            data = f.read()
                        self._cache[path] = (get_mime_type(path), compress(data) if self._use_compress else data)
                        self._timestamp[path] = timestamp
            path_list.pop(0)
        for key in old_keys:
            if key not in new_keys:
                try:
                    del self._cache[key]
                except KeyError:
                    pass
        return self._cache

    def get(self, filename: Union[str, Path]) -> Optional[Tuple[Optional[str], bytes]]:
        """
        The response is a tuple of mime-type and the content of the file.
        If can't find the file, return None.
        """
        res = self._cache.get(str(filename))
        if res is None:
            return None
        else:
            return res[0], decompress(res[1]) if self._use_compress else res[1]

# -------------------------------------------------------------------------- MocaDirectoryCache --
