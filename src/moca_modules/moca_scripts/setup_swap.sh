#! /bin/bash

# Only supports CentOS 8.

# The swap size.
size=32768  # 32G

# Setup swap.
dd if=/dev/zero of=/var/swapfile bs=1M count=${size}
mkswap /var/swapfile
chmod 600 /var/swapfile
swapon /var/swapfile
echo "/var/swapfile               swap                   swap    defaults        0 0" >> /etc/fstab
