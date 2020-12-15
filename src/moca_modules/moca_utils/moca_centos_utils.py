"""
The functions in this file, Only supports CentOS 8 and RHEL 8.
"""

# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Dict, List, Tuple
)
from subprocess import check_output, CalledProcessError
from .moca_utils import try_to_int

# -------------------------------------------------------------------------- Imports --

# -- Linux Utils --------------------------------------------------------------------------


def get_centos_cpu_info() -> Dict[int, Dict[str, Union[str, int]]]:
    """Get cpu info from `/proc/cpuinfo` """
    data: Dict[int, Dict[str, Union[str, int]]] = {
        0: {}
    }
    processor: int = 0
    res = check_output('cat /proc/cpuinfo', shell=True).decode().splitlines()
    for info in res:
        try:
            name, value = tuple(map(lambda i: try_to_int(i.strip()), info.split(':')))
        except ValueError:
            name = tuple(map(lambda i: try_to_int(i.strip()), info.split(':')))
            value = None
        if name == 'processor':
            processor = value
            data[processor] = {}
        data[processor][name] = value
    return data


def get_centos_cpu_model_name() -> Dict[int, str]:
    """Return the cpu model name.  {id, name}"""
    info: Dict[int, Dict[str, Union[str, int]]] = get_centos_cpu_info()
    data: Dict[int, str] = {}
    for cpu_id in info:
        data[cpu_id] = info[cpu_id]['model name']
    return data


def get_centos_cpu_mhz() -> Dict[int, str]:
    """Return the cpu MHz. {id, MHz}"""
    info = get_centos_cpu_info()
    data: Dict[int, str] = {}
    for cpu_id in info:
        data[cpu_id] = info[cpu_id]['cpu MHz']
    return data


def get_centos_cpu_cache_size() -> Dict[int, str]:
    """Return the cpu cache size. {id, cache_size}"""
    info = get_centos_cpu_info()
    data: Dict[int, str] = {}
    for cpu_id in info:
        data[cpu_id] = info[cpu_id]['cache size']
    return data


def get_centos_cpu_vendor_id() -> Dict[int, str]:
    """Return the cpu vendor id. {id, vendor_id}"""
    info = get_centos_cpu_info()
    data: Dict[int, str] = {}
    for cpu_id in info:
        data[cpu_id] = info[cpu_id]['vendor_id']
    return data


def get_centos_cpu_cores() -> Dict[int, str]:
    """Return the cpu cores number. {id, number}"""
    info = get_centos_cpu_info()
    data: Dict[int, str] = {}
    for cpu_id in info:
        data[cpu_id] = info[cpu_id]['cpu cores']
    return data


def __get_log(log_type: str) -> List[Tuple[str, str, str]]:  # time, user, ip
    """Format the log messages."""
    log: List[Tuple[str, str, str]] = []
    try:
        res = check_output(f'cat /var/log/secure | grep "sshd" | grep "{log_type}"', shell=True).decode().splitlines()
        for info_str in res:
            info = info_str.split()
            time = f'{info[0]} {info[1]} {info[2]}'
            user = 'unknown'
            ip = 'unknown'
            for index, item in enumerate(info):
                if item == 'from':
                    ip = info[index + 1]
                elif item == 'for':
                    user = info[index + 1]
            log.append((time, user, ip))
        return log
    except CalledProcessError:
        return []


def get_centos_ssh_login_log() -> Dict[str, List[Tuple[str, str, str]]]:
    """Return the ssh login log."""
    data: Dict[str, List[Tuple[str, str, str]]] = {  # time, user, ip
        'Accepted': __get_log('Accepted'),
        'Failed': __get_log('Failed'),
        'Invalid': __get_log('Invalid'),
    }
    return data


def get_centos_accepted_ssh_login_log() -> List[Tuple[str, str, str]]:  # time, user, ip
    """Return the accepted ssh login logs as a list."""
    return __get_log('Accepted')


def get_centos_failed_ssh_login_log() -> List[Tuple[str, str, str]]:  # time, user, ip
    """Return the failed ssh login logs as a list."""
    return __get_log('Failed')


def get_centos_invalid_ssh_login_log() -> List[Tuple[str, str, str]]:  # time, user, ip
    """Return the invalid ssh login logs as a list."""
    return __get_log('Invalid')


def get_centos_accepted_ssh_login_count() -> int:
    """Get the number of accepted login logs"""
    try:
        return int(check_output('grep -c Accepted /var/log/secure', shell=True).decode())
    except CalledProcessError:
        return 0


def get_centos_failed_ssh_login_count() -> int:
    """Get the number of failed login logs"""
    try:
        return int(check_output('grep -c Failed /var/log/secure', shell=True).decode())
    except CalledProcessError:
        return 0


def get_centos_invalid_ssh_login_count() -> int:
    """Get the number of invalid login logs"""
    try:
        return int(check_output('grep -c Invalid /var/log/secure', shell=True).decode())
    except CalledProcessError:
        return 0


def get_centos_recently_login_logs() -> List[str]:
    """Get the recently login logs"""
    try:
        res = []
        for item in check_output('last', shell=True).decode().splitlines():
            if item.startswith('reboot'):
                continue
            elif item == '':
                break
            else:
                res.append(item)
        return res
    except CalledProcessError:
        return []


def get_centos_kernel() -> str:
    """Get the kernel info."""
    return check_output('uname -r', shell=True).decode().strip()

# -------------------------------------------------------------------------- Linux Utils --
