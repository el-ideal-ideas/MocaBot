# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Any
)
from functools import partial
from pathlib import Path
from json import JSONDecodeError
from .MocaSynchronizedTextFile import MocaSynchronizedTextFile
from ..moca_core import ENCODING
try:
    from ujson import (
        dumps as __dumps, loads
    )

    dumps = partial(__dumps)
except (ImportError, ModuleNotFoundError):
    from json import (
        dumps as __dumps, loads
    )

    # This is done in order to ensure that the JSON response is
    # kept consistent across both ujson and inbuilt json usage.
    dumps = partial(__dumps, separators=(",", ":"))

# -------------------------------------------------------------------------- Imports --

# -- MocaSynchronizedJSONFile --------------------------------------------------------------------------


class MocaSynchronizedJSONFile(MocaSynchronizedTextFile):
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
        super().__init__(filename, check_interval, encoding=ENCODING, manual_reload=manual_reload)
        # set ensure_ascii flag
        self._ensure_ascii: bool = ensure_ascii
        # set sort_keys flag
        self._sort_keys: bool = sort_keys
        # set update time
        self._json_update_time: float = self._file_update_time
        # set json data
        if self._file_content == '':
            self.change_content('null')
        try:
            self._json = loads(self._file_content)
        except (TypeError, ValueError, JSONDecodeError):
            self._json = None

    def __str__(self) -> str:
        return f'MocaSynchronizedJSONFile: {self._filename}'

    @property
    def json(self) -> Any:
        """Get the loaded JSON data."""
        if self._json_update_time != self._file_update_time:
            try:
                self._json = loads(self._file_content)
                self._json_update_time = self._file_update_time
            except (TypeError, ValueError, JSONDecodeError):
                pass
        return self._json

    def change_json(self, data: Any) -> Any:
        """Change json data."""
        self.change_content(dumps(data, ensure_ascii=self._ensure_ascii, sort_keys=self._sort_keys, indent=2))
        return data

# -------------------------------------------------------------------------- MocaSynchronizedJSONFile --
