# -- Imports --------------------------------------------------------------------------

from typing import (
    List, Union, Any, Dict
)
from pathlib import Path
from time import sleep
from gc import collect
from threading import Thread
from ..moca_utils import moca_dump as dump, moca_load as load

# -------------------------------------------------------------------------- Imports --

# -- MocaMemoryController --------------------------------------------------------------------------


class MocaMemoryController:
    """
    -- english --------------------------------------------------------------------------
        This is the memory management module developed by el.ideal-ideas for Moca System.
        All data in this class have a life-time.
        When your use the data, the remaining-time will be reset.
        When the remaining-time is less than 0. MocaMemory will save the data to file, and remove it from memory.
        If you want to use the data that is not on memory, but in the cache file,
        MocaMemory will load the data automatically, and reset remaining-time.
        And MocaMemory can keep the data after your program is stopped. (method save_all_data_to_file)
    -- 日本語 --------------------------------------------------------------------------
        これはモカシステムのためにel.ideal-ideasによって開発されたメモリ管理モジュールである。
        このクラスによって管理されるすべてのデータはライフタイムを持っています。
        データは使用されたときに残り時間がリセットされます。
        残り時間が0以下になったとき、データはファイルに保存され、メモリから削除されます。
        ファイルに保存されメモリ上にないデータを使用しようとした場合、MocaMemoryは自動的にファイルからデータをロードして
        残り時間をリセットします。
        さらにメモリ上のデータをプログラム終了後の保持する手段としても使用できます。(メソッド save_all_data_to_file)
    -- 中文 --------------------------------------------------------------------------
        这是el.ideal-ideas为茉客系统开发的内存管理模块。
        由MocaMemory类管理的所有数据都有寿命。
        如果数据被调用，其剩余时间会被刷新。
        如果剩余时间变成0以下，数据就会被保存到文件并且从内存删除。
        当您调用被缓存到文件里的数据的时候。MocaMemory会自动从文件读取数据并刷新剩余时间。
        也可以用于在程序运行停止后用来保存内存里的数据。（方法 save_all_data_to_file）

    Attributes
    ----------
    _cache_dir: Path
        the path of the cache directory
    _storage: Dict[str, List[Any]]
        all data will save in this dictionary.
    """

    def __init__(
            self,
            cache_dir: Union[Path, str]
    ):
        """
        :param cache_dir: the path of cache directory.
        """
        # set cache_dir
        self._cache_dir: Path = Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        # set storage
        # {
        #   key: [life, remaining, value],
        # }
        self._storage: Dict[str, List[Any]] = {
            '__mochi__': [-1, -1, 'もっちもっちにゃんにゃん！']
        }
        # start life check timer
        self.__start_timer()

    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

    @property
    def storage(self) -> Dict[str, List[Any]]:
        return self._storage

    def save(self, key: str, value: Any, life: int = -1) -> None:
        """
        save a value to the data storage (in memory)
        :param key: key
        :param value: data
        :param life: life time (seconds), -1 means infinity.
        """
        # save the value
        # [life, remaining, value]
        self._storage[key] = [life, life, value]

    def get(self, key: str, default: Any = None) -> Any:
        """
        get a value from the data storage.
        :param key: key.
        :param default: if can't find the value, return default value.
        :return: target value or default value.
        """
        try:
            # reset remaining time
            self._storage[key][1] = self._storage[key][0]
            # return data
            return self._storage[key][2]
        except KeyError:  # can't found the value in memory
            # search in file directory
            if key in [path.name.split('.')[0] for path in self._cache_dir.glob('*.cache')]:
                # load file
                data = None
                try:
                    data = load(str(self._cache_dir.joinpath(key + '.cache')))
                except (PermissionError, FileNotFoundError, OSError):
                    pass
                if data is None:
                    # return default
                    return default
                else:
                    # reset remaining time
                    data[1] = data[0]
                    # set data into storage
                    self._storage[key] = data
                    # return data
                    return self._storage[key][2]
            else:
                # return default
                return default

    def __start_timer(self) -> None:
        """calculate remaining time"""

        def __timer():
            while True:
                sleep(1)
                remove_list = []
                for key in self._storage:
                    if self._storage[key][1] > 0:
                        self._storage[key][1] -= 1
                    else:
                        remove_list.append(key)
                for key in remove_list:
                    try:
                        dump(self._storage[key], str(self._cache_dir.joinpath(key + '.cache')))
                        del self._storage[key]
                    except KeyError:
                        pass
                collect()

        Thread(target=__timer, daemon=True).start()

    def remove(self, key: str) -> None:
        """
        Remove data from memory and disk
        :param key: the key of data.
        """
        # delete from memory
        try:
            del self._storage[key]
            collect()
        except KeyError:
            pass
        # delete from disk
        if key in [path.name.split('.')[0] for path in self._cache_dir.glob('*.cache')]:
            self._cache_dir.joinpath(key + '.cache').unlink()

    def save_all_data_to_file(self) -> None:
        """
        Save all data in memory to file
        """
        for key in self._storage:
            dump(self._storage[key], str(self._cache_dir.joinpath(key + '.cache')))

    def get_active_data_list(self) -> Dict[str, list]:
        """
        Return active data list info
        {
            key: [life, remaining]
        }
        """
        return {key: self._storage[key][0:2] for key in self._storage}

    def get_active_key_list(self) -> List[str]:
        """Return active key list"""
        return list(self._storage.keys())


# -------------------------------------------------------------------------- MocaMemoryController --
