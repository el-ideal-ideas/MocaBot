#!/usr/bin/env python3

"""
Generate a random string.
"""

# -- Imports --------------------------------------------------------------------------

from uuid import uuid4

# -------------------------------------------------------------------------- Imports --

if __name__ == '__main__':
    print(uuid4().hex, uuid4().hex, uuid4().hex, sep='')
