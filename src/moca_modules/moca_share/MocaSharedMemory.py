# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Any, Callable
)
from copy import copy
from multiprocessing import Manager
from .MocaMultiProcessLock import MocaMultiProcessLock

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

_DATA = 0
_LOCK = 1

# -------------------------------------------------------------------------- Variables --

# -- MocaSharedMemory --------------------------------------------------------------------------


class MocaSharedMemory:
    """
    This class can manage the shared data between processes.

    Attributes
    ----------
    self._manager: Manager
        the instance of multiprocessing.Manager.
    self._data_dict: dict
        {"some_name": self._manager.list([data_value, self._manager.RLock()])}

    """
    def __init__(
            self,
            other_shared_data_manager=None,
    ):
        self._data_dict: dict  # {"some_name": self._manager.list([data_value, self._manager.RLock()])}

        if other_shared_data_manager is None:
            self._manager = Manager()
            self._data_dict = self._manager.dict()  # Create a shared dict for data
        else:
            self._manager = other_shared_data_manager._manager
            self._data_dict = other_shared_data_manager._data_dict

    def get(self, name: str, default: Any = None) -> Any:
        """Get value (copy) by name."""
        data = self._data_dict.get(name, None)
        if data is not None:
            return data[_DATA]
        return copy(default)

    def set(self, name: str, value: Any) -> None:
        """Set value by name."""
        if name in self._data_dict:
            self._data_dict[name][_DATA] = value
        else:
            self._data_dict[name] = self._manager.list((value, self._manager.RLock()))
            
    def increment(self, name: str, value: int = 1) -> int:
        """Increment the value."""
        with self.lock(name):
            data = self.get(name, 0)
            data = data + value if isinstance(data, int) else 1
            self.set(name, data)
            return data

    def decrement(self, name: str, value: int) -> int:
        """Decrement the value."""
        with self.lock(name):
            data = self.get(name, 0)
            data = data - value if isinstance(data, int) else -1
            self.set(name, data)
            return data

    def change(self, name: str, func: Callable, *args, **kwargs) -> Any:
        """
        Use the current value call the function, and set the return value as the new value.
        If can't get a value by the `name` parameter, the current value will be None.
        :param name: the name of target data.
        :param func: the function to call.
        :param args: the arguments of the function.
        :param kwargs: the keyword arguments of the function.
        :return: the return value of the function.
        """
        with self.lock(name):
            data = self.get(name, None)
            new_value = func(data, *args, **kwargs)
            self.set(name, new_value)
            return new_value

    def lock(self, name):
        """
        Get a lock on the resource by name (with a wait if the lock is already captured).
        Returns ContextManager-object.
       """
        if name not in self._data_dict:
            self._data_dict[name] = self._manager.list((None, self._manager.RLock()))

        return MocaMultiProcessLock(self._data_dict[name][_LOCK], True)

    def try_lock(self, name):
        """
        Get a lock on the resource by name (without waiting, if the lock is already captured).
        Returns ContextManager-object.
        """
        if name not in self._data_dict:
            self._data_dict[name] = self._manager.list((None, self._manager.RLock()))

        return MocaMultiProcessLock(self._data_dict[name][_LOCK], False)

# -------------------------------------------------------------------------- MocaSharedMemory --
