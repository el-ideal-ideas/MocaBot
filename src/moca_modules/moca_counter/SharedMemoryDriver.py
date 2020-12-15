"""
This driver is too slow.
"""

# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Tuple
)
from uuid import uuid4
from .DriverInterface import DriverInterface
from ..moca_share import MocaSharedMemory

# -------------------------------------------------------------------------- Imports --

# -- Shared Memory Driver --------------------------------------------------------------------------


class SharedMemoryDriver(DriverInterface):
    """
    -- english --------------------------------------------------------------------------
    The driver use shared memory. for multi-process.
    -- 日本語 --------------------------------------------------------------------------
    このドライバーはマルチプロセス対応のため、共有メモリを使用します。
    -- 中文 --------------------------------------------------------------------------
    这个驱动为了对应多进程，采用了共享内存。

    Attributes
    ----------
    self._shared_memory: MocaSharedMemory
        a instance of MocaSharedMemory.
    self._prefix: str
        the prefix for data key.
    """

    NAME = 'SharedMemoryDriver'

    VERSION = '1.0.0'

    def __init__(
            self,
            shared_memory: MocaSharedMemory,
            prefix: Optional[str] = None
    ):
        """
        :param shared_memory: a instance of MocaSharedMemory.
        :param prefix: the prefix for data key.
        """
        self._shared_memory: MocaSharedMemory = shared_memory
        self._prefix: str = uuid4().hex if prefix is None else prefix

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
        cnt = self._shared_memory.increment(self._prefix + key, value)
        return True, cnt, 'success'

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
        self._shared_memory.set(self._prefix + key, value)
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
        cnt = self._shared_memory.get(self._prefix + key, default)
        return cnt, 'success'

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def clear(self,
              key: str) -> Tuple[bool, str]:
        """
        Clear the count by key.
        :param key: the key of the counter.
        :return: Tuple(status, message)
        """
        self._shared_memory.set(self._prefix + key, None)
        return True, 'success'

# -------------------------------------------------------------------------- Shared Memory Driver --
