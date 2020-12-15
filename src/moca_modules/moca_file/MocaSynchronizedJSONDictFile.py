# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Any, Dict, Optional, Callable, List, Set, Tuple
)
from pathlib import Path
from traceback import print_exc
from .MocaSynchronizedJSONFile import MocaSynchronizedJSONFile
from ..moca_core import IS_DEBUG, MOCA_NULL
from ..moca_utils import print_error

# -------------------------------------------------------------------------- Imports --

# -- MocaSynchronizedJSONDictFile --------------------------------------------------------------------------


class MocaSynchronizedJSONDictFile(MocaSynchronizedJSONFile):
    """
    This class will synchronize with the target json file.
    指定のJSONファイルとメモリ上のデータを同期させる。
    让指定的JSON文件和内存上的数据同步。

    Attributes
    ----------
    self._json_update_time: float
        json update time.
    self._json
        the json data.
    self._ensure_ascii: bool
        If ensure_ascii is false, then the strings written to ``fp`` can contain non-ASCII characters.
    self._sort_keys: bool
        if sort_keys is true, then the output of dictionaries will be sorted by key.
    self._handlers: Dict[str, List]
        the handlers
    self._handled_keys: Dict[str, Set[str]]
        the keys handled by handlers.
    """

    def __init__(
            self,
            filename: Union[str, Path],
            check_interval: float = 0.1,
            ensure_ascii: bool = False,
            sort_keys: bool = True,
            manual_reload: bool = False,
    ):
        """
        :param filename: the file name of the target file.
        :param check_interval: the interval to check file (seconds).
        :param ensure_ascii: If ensure_ascii is false,
               then the strings written to file can contain non-ASCII characters.
        :param sort_keys: if sort_keys is true, then the output of dictionaries will be sorted by key.
        :param manual_reload: don't create the reload timer thread. You need run reload_file method manually.
        """
        super().__init__(
            filename, check_interval, ensure_ascii=ensure_ascii, sort_keys=sort_keys, manual_reload=manual_reload
        )
        # If the json data is not a dictionary, change the data to a empty dictionary.
        if not isinstance(self.json, dict):
            self.change_json({})
        # initialize handlers dictionary
        self._handlers: Dict[str, List] = {}
        # initialize handled keys list
        self._handled_keys: Dict[str, Set[str]] = {}

    def __str__(self) -> str:
        return f'MocaSynchronizedJSONDictFile: {self._filename}'

    @property
    def dict(self) -> Dict:
        return self.json

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key. If can't found the key, return default."""
        return self.json.get(key, default)

    def get_all(self) -> Dict:
        """Return all items."""
        return self.json

    def check(self, key: str, value: Any) -> bool:
        """if this value is same as the value in the file, return True."""
        return value == self.get(key)

    def set(self, key: str, value: Any) -> Dict:
        """Set a value by key."""
        if value != self.json.get(key, MOCA_NULL):
            self._run_handler_one(key, self.json.get(key, MOCA_NULL), value)
            json = self.json
            json[key] = value
            self.change_json(json)
        return self.json

    def remove(self, key: str) -> Dict:
        """Remove a value by key."""
        json = self.json
        try:
            del json[key]
        except KeyError:
            pass
        self.change_json(json)
        return self.json

    def clear_dict(self) -> Dict:
        """Clear the dictionary."""
        self.change_json({})
        return self.json

    def reload_file(self) -> str:
        """Reload the file manually."""
        try:
            old = self.dict
            res = super().reload_file()
            new = self.dict
            if old != new:
                self._run_handler_total(old, new)
            return res
        except AttributeError:
            return super().reload_file()

    def add_handler(
            self,
            name: str,
            keys: Union[List[str], str],
            handler: Callable,
            args: Tuple = (),
            kwargs: Dict = {}
    ) -> None:
        """
        Add a handler to do something when the config value was changed.
        :param name: the name of this handler. if same name is already exists, overwrite it.
        :param keys: the keys of the config.
        :param handler: the handler function.  arguments(the_updated_key, old_value, new_value, *args, **kwargs)
        :param args: arguments to the handler.
        :param kwargs: keyword arguments to the handler.
        :return: None
        """
        self._handlers[name] = [keys, handler, args, kwargs]
        if isinstance(keys, str):
            try:
                self._handled_keys[keys].add(name)
            except KeyError:
                self._handled_keys[keys] = {name}
        else:
            for key in keys:
                try:
                    self._handled_keys[key].add(name)
                except KeyError:
                    self._handled_keys[key] = {name}

    def remove_handler(self, name: str) -> None:
        """Remove the registered handler"""
        try:
            del self._handlers[name]
            for key in self._handled_keys:
                try:
                    self._handled_keys[key].remove(name)
                except KeyError:
                    pass
        except KeyError:
            pass

    def get_handler(self, name: str) -> Optional[Callable]:
        """Get the registered handler"""
        try:
            return self._handlers[name][1]
        except KeyError:
            return None

    def _run_handler_total(self, old_cache: Dict, new_cache: Dict) -> None:
        """Run the handlers if needed."""
        for key in self._handled_keys:
            try:
                if old_cache[key] != new_cache[key]:
                    for name in self._handled_keys[key]:
                        try:
                            self._handlers[name][1](key,
                                                    old_cache[key],
                                                    new_cache[key],
                                                    *self._handlers[name][2],
                                                    **self._handlers[name][3])
                        except SystemExit:
                            raise
                        except Exception as e:
                            print_error(f'Some error occurred in the handler of MocaSynchronizedJSONDictFile. '
                                        f'<Exception: {e}>')
                            print_exc()

            except KeyError:
                pass

    def _run_handler_one(self, key: str, old_value: Any, new_value: Any) -> None:
        """Run the handlers if needed."""
        try:
            for name in self._handled_keys[key]:
                try:
                    self._handlers[name][1](key,
                                            old_value,
                                            new_value,
                                            *self._handlers[name][2],
                                            **self._handlers[name][3])
                except SystemExit:
                    raise
                except Exception as e:
                    if IS_DEBUG:
                        print_error(f'Some error occurred in the handler of MocaSynchronizedJSONDictFile. '
                                    f'<Exception: {e}>')
        except KeyError:
            pass

# -------------------------------------------------------------------------- MocaSynchronizedJSONDictFile --
