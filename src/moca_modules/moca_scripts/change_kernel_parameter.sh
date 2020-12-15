#! /bin/bash

# Only supports CentOS 8.

# Change kernel parameters.
echo 1048576 > /proc/sys/fs/inotify/max_user_watches
sysctl -w net.core.default_qdisc=fq
sysctl -w net.ipv4.tcp_congestion_control=bbr
sysctl -w net.ipv4.ip_local_port_range='1024 65535'
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.ipv4.tcp_keepalive_probes=5
sysctl -w net.ipv4.tcp_max_tw_buckets=65536
sysctl -w net.ipv4.tcp_fin_timeout=30
sysctl -w net.ipv4.tcp_rfc1337=1
sysctl -w net.ipv4.conf.all.rp_filter=1
sysctl -w net.ipv4.tcp_syncookies=1
sysctl -w net.ipv4.tcp_timestamps=0
sysctl -w net.ipv4.icmp_echo_ignore_broadcasts=1
sysctl -w net.ipv4.tcp_syn_retries=1
sysctl -w net.ipv4.tcp_synack_retries=1
sysctl -w net.core.netdev_max_backlog=65536
sysctl -w net.ipv4.tcp_max_syn_backlog=65536
sysctl -w net.core.somaxconn=65535
sysctl -w kernel.panic=30
sysctl -w vm.panic_on_oom=1
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w vm.swappiness=10
sysctl -w kernel.threads-max=600000
sysctl -w kernel.pid_max=600000
sysctl -w vm.max_map_count=1200000
sysctl -w fs.file-max=6815744
