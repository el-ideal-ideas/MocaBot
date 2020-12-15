#! /bin/bash

# Only supports CentOS 8.

# The version number of python.
version="3.9.0"

# Install dependencies
dnf -y update
dnf -y groupinstall "Development Tools"
dnf -y install sqlite sqlite-libs sqlite-devel xz-devel
dnf -y install openssl-devel bzip2-devel libffi-devel

# Get the source code of python.
wget "https://www.python.org/ftp/python/${version}/Python-${version}.tgz"

# Decompress the source code.
tar xvf "Python-${version}.tgz"

# Compile the source code.
cd "Python-${version}/" || echo "Error: Can't change directory."
./configure --enable-optimizations
make altinstall

# Update pip
python3.9 -m pip install pip --upgrade
