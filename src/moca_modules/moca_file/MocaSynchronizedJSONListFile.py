# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Any, List
)
from pathlib import Path
from .MocaSynchronizedJSONFile import MocaSynchronizedJSONFile

# -------------------------------------------------------------------------- Imports --

# -- MocaSynchronizedJSONListFile --------------------------------------------------------------------------


class MocaSynchronizedJSONListFile(MocaSynchronizedJSONFile):
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
    self._remove_duplicates: bool
        remove duplicate items, use list as a set.
    """

    def __init__(
            self,
            filename: Union[str, Path],
            check_interval: float = 0.1,
            ensure_ascii: bool = False,
            remove_duplicates: bool = False,
            manual_reload: bool = False,
    ):
        """
        :param filename: the file name of the target file.
        :param check_interval: the interval to check file (seconds).
        :param ensure_ascii: If ensure_ascii is false,
               then the strings written to file can contain non-ASCII characters.
        :param remove_duplicates: remove duplicate items, use list as a set.
        :param manual_reload: don't create the reload timer thread. You need run reload_file method manually.
        """
        self._remove_duplicates: bool = remove_duplicates
        super().__init__(filename, check_interval, ensure_ascii=ensure_ascii, manual_reload=manual_reload)
        # If the json data is not a list, change the data to a empty list.
        if not isinstance(self.json, list):
            self.change_json([])

    def __str__(self) -> str:
        return f'MocaSynchronizedJSONListFile: {self._filename}'

    def change_json(self, data: list) -> Any:
        """Change json data."""
        if self._remove_duplicates:
            return super(MocaSynchronizedJSONListFile, self).change_json(list(set(data)))
        else:
            return super(MocaSynchronizedJSONListFile, self).change_json(data)

    @property
    def list(self) -> List:
        return self.json

    def is_in(self, item: Any) -> bool:
        """If the item is in the list, return True."""
        return item in self.json

    def slice(self, start: int, stop: int) -> List:
        """Slice the list object and update the file."""
        json = self.json[start:stop]
        self.change_json(json)
        return json

    def append(self, item: Any) -> List:
        """Appends the given item to the list object and update the file."""
        json = self.json
        json.append(item)
        self.change_json(json)
        return json

    def extend(self, data: List) -> List:
        """Extends the list object and update the file."""
        json = self.json
        json.extend(data)
        self.change_json(json)
        return json

    def insert(self, index: int, item: Any) -> List:
        """Inserts the given item into the list object and update the file."""
        json = self.json
        json.insert(index, item)
        self.change_json(json)
        return json

    def remove(self, item: Any) -> List:
        """Removes the given item from the list object and update the file."""
        json = self.json
        json.remove(item)
        self.change_json(json)
        return json

    def pop(self, index: int = -1) -> Any:
        """Pop the item from the list object and update the file."""
        json = self.json
        return json.pop(index)

    def sort(self, *args, **kwargs) -> List:
        """Sort the list object and update the file."""
        json = self.json
        json.sort(*args, **kwargs)
        self.change_json(json)
        return json

    def clear_list(self) -> None:
        """Clear the list."""
        self.change_json([])

# -------------------------------------------------------------------------- MocaSynchronizedJSONListFile --
