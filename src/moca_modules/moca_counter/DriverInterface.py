# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Tuple
)
from abc import ABCMeta, abstractmethod

# -------------------------------------------------------------------------- Imports --

# -- Async Redis Driver --------------------------------------------------------------------------


class DriverInterface(metaclass=ABCMeta):
    """
    -- english --------------------------------------------------------------------------
    All synchronized drivers must implement this interface.
    -- 日本語 --------------------------------------------------------------------------
    すべての同期ドライバーはこの抽象クラスを継承しなくてはいけない。
    -- 中文 --------------------------------------------------------------------------
    所有的同步驱动必须继承这个抽象类。

    """

    NAME = 'DriverInterface'

    VERSION = '1.0.0'

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @abstractmethod
    def add(self,
            key: str,
            value: int = 1) -> Tuple[bool, Optional[int], str]:
        """
        Add count by key.
        :param key: the key of the counter.
        :param value: the value to add.
        :return: Tuple(status, count, message) If can't get the value of counter, count will be None.
        """
        pass

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @abstractmethod
    def set(self,
            key: str,
            value: int) -> Tuple[bool, str]:
        """
        Set count by key.
        :param key: the key of the counter.
        :param value: the value to set.
        :return: Tuple(status, message)
        """
        pass

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @abstractmethod
    def get(self,
            key: str,
            default: Optional[int] = None) -> Tuple[Optional[int], str]:
        """
        Get the count by key.
        :param key: the key of the counter.
        :param default: the default value.
        :return: Tuple(value, message). if some error occurred, the response value will be default value.
        """
        pass

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @abstractmethod
    def clear(self,
              key: str) -> Tuple[bool, str]:
        """
        Clear the count by key.
        :param key: the key of the counter.
        :return: Tuple(status, message)
        """
        pass

# -------------------------------------------------------------------------- Async Redis Driver --
