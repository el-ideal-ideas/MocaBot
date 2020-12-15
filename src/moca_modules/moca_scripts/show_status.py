#!/usr/bin/env python3

"""
Show System Status.
Only supports CentOS 8.
"""

# -- Imports --------------------------------------------------------------------------

from subprocess import check_output, call
from os import getuid
from pathlib import Path
from typing import (
    List
)

# -------------------------------------------------------------------------- Imports --

# -- Show Status --------------------------------------------------------------------------


def show_status() -> None:
    if not Path('/etc/redhat-release').is_file():
        print('This command only supports CentOS and Red Hat Enterprise Linux.')
        return None
    date: str = check_output('date "+%F %T"', shell=True).decode().strip()
    head: str = f'System Time: {date}'
    kernel: str = check_output('uname -r', shell=True).decode().strip()
    hostname: str = check_output('echo $HOSTNAME', shell=True).decode().strip()
    load1, load5, load15, *_ = check_output('cat /proc/loadavg', shell=True).decode().strip().split()
    uptime: int = int(check_output("cat /proc/uptime | cut -f1 -d.", shell=True).decode().strip())
    up_days: int = int(uptime/60/60/24)
    up_hours: int = int(uptime / 60 / 60 % 24)
    up_minutes: int = int(uptime / 60 % 60)
    up_seconds: int = int(uptime % 60)
    memory_info: List[str] = check_output('free', shell=True).decode().splitlines()[1].split()
    swap_info: List[str] = check_output('free', shell=True).decode().splitlines()[2].split()
    memory_percent: float = int(memory_info[2]) / int(memory_info[1]) * 100
    swap_percent: float = int(swap_info[2]) / int(swap_info[1]) * 100
    process_count: str = check_output("ps aux | wc -l", shell=True).decode().strip()
    user_count: str = check_output('users | wc -w', shell=True).decode().strip()
    user: str = check_output('whoami', shell=True).decode().strip()
    time_zone: str = check_output('timedatectl | grep "Time zone"', shell=True).decode().split()[2]
    file_system: List[List[str]] = [
        item.split() for item in check_output("df -h", shell=True).decode().splitlines() if item.startswith('/dev')
    ]
    network_interface_script = """
    INTERFACES=$(ip -4 ad | grep 'state ' | awk -F":" '!/^[0-9]*: ?lo/ {print $2}')
    printf "Interface\tMAC Address\t\tIP Address\n"
    for i in $INTERFACES
    do
        MAC=$(ip ad show dev $i | grep "link/ether" | awk '{print $2}')
        IP=$(ip ad show dev $i | awk '/inet / {print $2}')
        printf $i"\t\t"$MAC"\t$IP\n"
    done
    """
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("""\033[1;36m
    □□□          □□□□                                        
    □□□□         □□□□                                        
    □□□□        □□□□□                                        
    □□ □□       □□ □□                                        
    □□ □□       □□□□□                                        
    □□ □□      □□ □□□      □□□□□         □□□□□        □□□□□  
    □□  □□     □□ □□□     □□□□□□□□      □□□□□□□□     □□□□□□□ 
    □□  □□    □□  □□□    □□□    □□□    □□□    □□    □□□   □□□
    □□  □□□   □□  □□□    □□      □□    □□                  □□
    □□   □□   □□  □□□   □□□      □□□  □□                   □□
    □□   □□  □□   □□□   □□        □□  □□             □□□□□□□□
    □□    □□ □□   □□□   □□        □□  □□            □□□    □□
    □□    □□ □    □□□   □□       □□□  □□           □□□     □□
    □□    □□□□    □□□    □□      □□    □□          □□     □□□
    □□     □□□    □□□    □□□    □□□    □□□    □□□  □□□   □□□□
    □□     □□     □□□     □□□□□□□□      □□□□□□□□    □□□□□□□□□
     □             □       □□□□□         □□□□□       □□□□□ □□
    \033[0m""")
    print()
    call('cat /etc/redhat-release', shell=True)
    print(head)
    print("----------------------------------------------")
    print(f"Kernel Version:\t\t{kernel}")
    print(f"HostName:\t\t{hostname}")
    print(f"System Load:\t\t{load1} {load5} {load15}")
    print(f"System Uptime:\t\t{up_days}days {up_hours}hours {up_minutes}minutes {up_seconds}seconds")
    print(f"Memory Usage:\t\t{round(memory_percent, 1)}%\t\t\tSwap Usage:\t{round(swap_percent, 1)}%")
    print(f"Login Users:\t\t{user_count}")
    print(f"User:\t\t\t{user}")
    print(f"Running Process:\t{process_count}")
    print(f"Time Zone:\t\t{time_zone}")
    print("----------------------------------------------")
    print("Filesystem\tUsage")
    for data in file_system:
        print(f"{data[5]}\t\t{data[4]}")
    call(network_interface_script, shell=True)
    print("----------------------------------------------")
    print("Login Log")
    call('last | head -5', shell=True)
    print("----------------------------------------------")
    print("Security Log (only root user)")
    if getuid() == 0:
        call("cat /var/log/secure | grep -e Invalid -e Failed | tail -n 5", shell=True)
    else:
        print('Your are not root user.')
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


# -------------------------------------------------------------------------- Show Status --

# -- Run --------------------------------------------------------------------------


if __name__ == '__main__':
    show_status()

# -------------------------------------------------------------------------- Run --
