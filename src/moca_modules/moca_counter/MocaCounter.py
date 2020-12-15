# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Tuple
)
from .AsyncInMemoryDriver import AsyncInMemoryDriver
from .DriverInterface import DriverInterface
from .InMemoryDriver import InMemoryDriver
from .AsyncInMemoryDriver import AsyncDriverInterface

# -------------------------------------------------------------------------- Imports --

# -- Main Class --------------------------------------------------------------------------


class MocaCounter(object):
    """
    -- english --------------------------------------------------------------------------
    This is a simple counter module for MocaSystem. Developed by el.ideal-ideas for Moca System.
    -- 日本語 --------------------------------------------------------------------------
    これはel.ideal-ideasによって開発されたモカシステムのためのシンプルなカウンターモジュールです。
    -- 简体中文 --------------------------------------------------------------------------
    这是el.ideal-ideas为茉客系统开发的计数器模块。

    Attributes
    ----------
    _driver: DriverInterface
        the driver of this instance.

    """

    def __init__(self, driver: Optional[DriverInterface]):
        """
        :param driver: an instance of synchronized driver.
        Arise
        -----
            TypeError: if type of argument is incorrect.
        """
        self._driver: DriverInterface
        if driver is None:
            self._driver = InMemoryDriver()
        else:
            if isinstance(driver, DriverInterface):
                self._driver = driver
            else:
                raise TypeError("Argument type error."
                                "Expected driver: Optional[DriverInterface] "
                                f"But Received: driver: {type(driver)}")

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
        return self._driver.add(key, value)

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
        return self._driver.set(key, value)

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
        return self._driver.get(key, default)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def clear(self,
              key: str) -> Tuple[bool, str]:
        """
        Clear the count by key.
        :param key: the key of the counter.
        :return: Tuple(status, message)
        """
        return self._driver.clear(key)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def info(self) -> str:
        return self._driver.NAME + ': ' + self._driver.VERSION

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


class MocaAsyncCounter(object):
    """
    -- english --------------------------------------------------------------------------
    This is a simple counter module for MocaSystem. Developed by el.ideal-ideas for Moca System.
    -- 日本語 --------------------------------------------------------------------------
    これはel.ideal-ideasによって開発されたモカシステムのためのシンプルなカウンターモジュールです。
    -- 简体中文 --------------------------------------------------------------------------
    这是el.ideal-ideas为茉客系统开发的计数器模块。

    Attributes
    ----------
    self._driver: DriverInterface
        the driver of this instance.

    """

    def __init__(self, driver: Optional[AsyncDriverInterface]):
        """
        :param driver: an instance of synchronized driver.
        Arise
        -----
            TypeError: if type of argument is incorrect.
        """
        self._driver: AsyncDriverInterface
        if driver is None:
            self._driver = AsyncInMemoryDriver()
        else:
            if isinstance(driver, AsyncDriverInterface):
                self._driver = driver
            else:
                raise TypeError("Argument type error."
                                "Expected driver: Optional[AsyncDriverInterface] "
                                f"But Received: driver: {type(driver)}")

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def add(self,
                  key: str,
                  value: int = 1) -> Tuple[bool, Optional[int], str]:
        """
        Add count by key.
        :param key: the key of the counter.
        :param value: the value to add.
        :return: Tuple(status, count, message) If can't get the value of counter, count will be None.
        """
        return await self._driver.add(key, value)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def set(self,
                  key: str,
                  value: int) -> Tuple[bool, str]:
        """
        Set count by key.
        :param key: the key of the counter.
        :param value: the value to set.
        :return: Tuple(status, message)
        """
        return await self._driver.set(key, value)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def get(self,
                  key: str,
                  default: Optional[int] = None) -> Tuple[Optional[int], str]:
        """
        Get the count by key.
        :param key: the key of the counter.
        :param default: the default value.
        :return: Tuple(value, message). if some error occurred, the response value will be default value.
        """
        return await self._driver.get(key, default)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def clear(self,
                    key: str) -> Tuple[bool, str]:
        """
        Clear the count by key.
        :param key: the key of the counter.
        :return: Tuple(status, message)
        """
        return await self._driver.clear(key)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def info(self) -> str:
        return self._driver.NAME + ': ' + self._driver.VERSION

# -------------------------------------------------------------------------- Main Class --
