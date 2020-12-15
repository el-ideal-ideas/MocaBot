# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Any, Union
)
from pathlib import Path
from gc import collect
from threading import Thread
from time import sleep
try:
    from cloudpickle import dump, load
except (ImportError, ModuleNotFoundError):
    from pickle import dump, load

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

# -------------------------------------------------------------------------- Variables --

# -- MocaSimpleCache --------------------------------------------------------------------------


class MocaSimpleCache:
    """
    -- english --------------------------------------------------------------------------
    This is the first in first out cache module developed by el.ideal-ideas for Moca System.
    The pool-size is the maximum number of cache.
    System will remove old cache (one page) from memory when the cache is full.
    And you can save the cache to file, or load from file manually.
    -- 日本語 --------------------------------------------------------------------------
    これはモカシステムのためにel.ideal-ideasによって開発された先入れ先出しのキャッシュモジュールである。
    プールサイズは保存できるキャッシュの総数です。
    キャッシュがいっぱいになると、古いものから1ページ分削除されます。
    手動でキャッシュをファイルに保存したり、ファイルから読み込んだりすることも出来ます。
    -- 中文 --------------------------------------------------------------------------
    这是el.ideal-ideas为茉客系统开发的先入先出的缓存模块。
    pool-size的值是可以保存的缓存数量的上限。
    如果缓存到达上限，系统会从旧的缓存开始删除一页(page-size)的缓存。
    您也可以手动把缓存保存到文件，或者从文件读取缓存。

    Attributes
    ----------
    _storage: dict
        the cache storage of this instance.
    _pool_size: int
        the cache pool size of this instance.
    _page_size: int
        the cache page size of this instance.
    _timer: float
        the auto clear timer.
    _timer_thread: Optional[Thread]
        the timer thread.
    """

    DEFAULT_POOL_SIZE: int = 10000
    DEFAULT_PAGE_SIZE: int = 1000

    def __init__(
            self,
            pool_size: Optional[int] = None,
            page_size: Optional[int] = None
    ):
        """
        :param pool_size: The pool size of this instance.
        :param page_size: The page size of this instance.
        """
        # set cache storage
        self._storage: dict = {}
        # set pool size ¥
        self._pool_size: int = pool_size if pool_size is not None else self.DEFAULT_POOL_SIZE
        # set page size
        self._page_size: int = page_size if page_size is not None else self.DEFAULT_PAGE_SIZE
        # initialize timer variable
        self._timer: float = -1
        self._timer_thread: Optional[Thread] = None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def remove_old_data(self,
                        limit: int) -> None:
        """remove old data in self._storage"""
        # remove old keys
        for key in list(self._storage.keys())[:limit]:
            try:
                del self._storage[key]
            except KeyError:
                pass
        collect()

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def start_auto_clear_timer(self, seconds: float) -> None:
        """Set a timer to clear storage automatically."""

        self._timer = seconds
        if self._timer_thread is None:
            def __timer(instance: MocaSimpleCache) -> None:
                while True:
                    if instance._timer == -1:
                        sleep(1)
                    else:
                        sleep(instance._timer)
                        instance._storage.clear()

            self._timer_thread = Thread(target=__timer, args=(self,))
            self._timer_thread.start()

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def stop_auto_clear_timer(self) -> None:
        """stop the auto clear timer"""
        self._timer = -1

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set(self,
            key: str,
            value: Any) -> None:
        """Add a cache"""
        # check storage size
        if len(self._storage) >= self._pool_size:
            self.remove_old_data(self._page_size)
        # save value
        self._storage[key] = value

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get(self,
            key: str,
            res_type: Any = any,
            default: Any = None) -> Any:
        """
        Get the cache
        :param key: the key of data.
        :param res_type: response type, if res_type is not any, system will check the type.
        :param default: if can't found the data, or the response type is incorrect, return default value.
        :return: the data or default data.
        """
        try:
            data = self._storage[key]
            if (res_type == any) or isinstance(data, res_type):
                return data
            else:
                return default
        except KeyError:
            return default

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def remove_cache(self,
                     key: str) -> None:
        """Remove data from cache"""
        try:
            del self._storage[key]
        except KeyError:
            pass

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def storage_size(self) -> int:
        """Return self._storage size"""
        return len(self._storage)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def pool_size(self) -> int:
        """Return the pool size"""
        return self._pool_size

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def page_size(self) -> int:
        """Return the page size"""
        return self._page_size

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def change_pool_size(self,
                         size: int) -> None:
        """Change the pool size"""
        self._pool_size = size

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def change_page_size(self,
                         size: int) -> None:
        """Change the page size"""
        self._page_size = size

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def clear_all(self) -> None:
        """Clear all cache"""
        self._storage = {}

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def save_cache_to_file(self,
                           filename: Union[Path, str]) -> bool:
        """
        Save all cache into file.
        :param filename: file path of the cache file.
        :return: status, [success] or [failed]
        """
        try:
            with open(str(filename), mode='wb') as cache_file:
                dump(self._storage, cache_file)
            return True
        except (PermissionError, OSError):
            return False

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def load_cache_from_file(self,
                             filename: Union[Path, str]) -> bool:
        """
        Load the cache from file.
        :param filename: file path of the cache file.
        :return: status, [success] or [failed]
        """
        try:
            with open(str(filename), mode='rb') as cache_file:
                self._storage = load(cache_file)
            return True
        except (FileNotFoundError, PermissionError, OSError):
            return False

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

# -------------------------------------------------------------------------- MocaSimpleCache --
