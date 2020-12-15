# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Tuple
)
from .DriverInterface import DriverInterface

# -------------------------------------------------------------------------- Imports --

# -- In Memory Driver --------------------------------------------------------------------------


class InMemoryDriver(DriverInterface):
    """
    -- english --------------------------------------------------------------------------
    This is a in-memory driver.
    -- 日本語 --------------------------------------------------------------------------
    これはインメモリドライバーです。
    -- 中文 --------------------------------------------------------------------------
    这是内存驱动。

    Attributes
    ----------
    self._storage: dict
        all date will be stored in this variable.

    """

    NAME = 'InMemoryDriver'

    VERSION = '1.0.0'

    def __init__(self):
        self._storage: dict = {}

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def add(self,
            key: str,
            value: int = 1) -> Tuple[bool, Optional[int], str]:
        """
        Add count by key.
        :param key: the key of the counter.
        :param value: the value to add.
        :return: Tuple(status, count, message) If can't get the value of counter, count will be None.
        """
        try:
            self._storage[key] += value
            return True, self._storage[key], 'success'
        except KeyError:
            self._storage[key] = 1
            return True, self._storage[key], 'success'

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set(self,
            key: str,
            value: int) -> Tuple[bool, str]:
        """
        Set count by key.
        :param key: the key of the counter.
        :param value: the value to set.
        :return: Tuple(status, message)
        """
        self._storage[key] = value
        return True, 'success'

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get(self,
            key: str,
            default: Optional[int] = None) -> Tuple[Optional[int], str]:
        """
        Get the count by key.
        :param key: the key of the counter.
        :param default: the default value.
        :return: Tuple(value, message). if some error occurred, the response value will be default value.
        """
        try:
            return self._storage[key], 'success'
        except KeyError:
            return default, 'success'

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def clear(self,
              key: str) -> Tuple[bool, str]:
        """
        Clear the count by key.
        :param key: the key of the counter.
        :return: Tuple(status, message)
        """
        try:
            del self._storage[key]
        except KeyError:
            pass
        return True, 'success'

# -------------------------------------------------------------------------- In Memory Driver --
