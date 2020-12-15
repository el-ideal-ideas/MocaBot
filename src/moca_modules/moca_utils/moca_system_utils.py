# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, List, Union, Dict
)
from psutil import (
    cpu_count, cpu_percent, virtual_memory, swap_memory, disk_partitions, disk_usage, Process
)
from os import getpid
from multiprocessing import current_process
from threading import get_ident
from shutil import copytree, rmtree
from pathlib import Path
from ..moca_core import SELF_PATH, IS_WIN, PROCESS_ID

# -------------------------------------------------------------------------- Imports --

# -- System Utils --------------------------------------------------------------------------


def get_logical_cpu_count() -> Optional[int]:
    """Get the number of logical CPU cores"""
    return cpu_count(logical=True)


def get_cpu_count() -> Optional[int]:
    """Get the number of physical CPU cores"""
    return cpu_count(logical=False)


def get_cpu_percent() -> float:
    """Get the percentage of the cpu usage."""
    return cpu_percent(interval=1, percpu=False)


def get_cpu_percent_per_cpu() -> List[float]:
    """Get the percentage of the cpu usage per cpu."""
    return cpu_percent(interval=1, percpu=True)


def get_total_memory() -> int:
    """Get the total memory size in bytes."""
    return virtual_memory().total


def get_free_memory() -> int:
    """Get the free memory size in bytes."""
    return virtual_memory().available


def get_used_memory() -> int:
    """Get the used memory size in bytes."""
    return virtual_memory().used


def get_memory_percent() -> float:
    """Get the percentage of the memory usage."""
    return virtual_memory().percent


def get_self_used_memory() -> int:
    """Get the size of memory used by this process in bytes."""
    return Process(getpid()).memory_info().rss


def get_self_used_memory_percent() -> float:
    """Get the percentage of the memory used by this process."""
    return Process(getpid()).memory_percent()


def get_memory_info() -> Dict[str, Union[int, float]]:
    """Get the memory information."""
    vm = virtual_memory()
    return {
        'total': vm.total,
        'available': vm.available,
        'used': vm.used,
        'percent': vm.percent,
    }


def get_total_swap_memory() -> int:
    """Get the total swap memory size in bytes."""
    return swap_memory().total


def get_free_swap_memory() -> int:
    """Get the free swap memory size in bytes."""
    return swap_memory().free


def get_used_swap_memory() -> int:
    """Get the used swap memory size in bytes."""
    return swap_memory().used


def get_swap_memory_percent() -> float:
    """Get the percentage of the swap memory usage."""
    return swap_memory().percent


def get_swap_memory_info() -> Dict[str, Union[int, float]]:
    """Get the swap memory information."""
    vsm = swap_memory()
    return {
        'total': vsm.total,
        'free': vsm.free,
        'used': vsm.used,
        'percent': vsm.percent,
    }


def get_disk_usage() -> Dict[str, Dict[str, Union[str, int]]]:
    return {disk_part.device: {
        'mountpoint': disk_part.mountpoint,
        'fstype': disk_part.fstype,
        'opts': disk_part.opts,
        'total': disk_usage(disk_part.mountpoint).total,
        'used': disk_usage(disk_part.mountpoint).used,
        'free': disk_usage(disk_part.mountpoint).free,
        'percent': disk_usage(disk_part.mountpoint).percent,
    } for disk_part in disk_partitions()}


def get_my_username() -> str:
    """Get the username of this process."""
    return Process(getpid()).username()


def is_root() -> bool:
    """If the process is running by root user, return True."""
    return get_my_username() == 'root'


def get_my_pid() -> Optional[int]:
    """Get the pid of current process."""
    return current_process().pid


def get_my_tid() -> int:
    """Get the id of current thread."""
    return get_ident()


def add_moca_modules_to_system(key: str = '') -> None:
    """
    Copy moca_modules to /opt/python_modules/moca_modules or `C:\\Program Files\\python_modules\\moca_modules`
    """
    __key = key if key == '' else '_' + key
    path = Path('C:\\Program Files\\python_modules\\moca_modules' + __key) if IS_WIN\
        else Path('/opt/python_modules/moca_modules' + __key)
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        rmtree(str(path))
    copytree(str(SELF_PATH), str(path))


def is_main_process() -> bool:
    """If current process is a main process. Return True"""
    return current_process().pid == PROCESS_ID

# -------------------------------------------------------------------------- System Utils --
