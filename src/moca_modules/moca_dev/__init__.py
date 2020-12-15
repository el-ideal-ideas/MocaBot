# -- Imports --------------------------------------------------------------------------

from benchmarker import Benchmarker, BenchmarkerError
from .compress_test import compress_test
from .json_test import json_test
from .benchmark import string_bench
from .bench_funcs import (
    fibonacci_loop, fibonacci_sym, fibonacci_recursion,
    fibonacci_list_loop, fibonacci_list_sym, fibonacci_list_recursion
)

# -------------------------------------------------------------------------- Imports --

"""
This module provides some functions for testing.

Requirements
------------
Benchmarker
    Benchmarker.py is an awesome benchmarking tool for Python.
orjson
    Fast, correct Python JSON library supporting dataclasses, datetimes, and numpy
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
simplejson
    simplejson is a simple, fast, extensible JSON encoder/decoder for Python
python-rapidjson
    Python wrapper around rapidjson
brotli
    Brotli compression format
sympy
    A computer algebra system written in pure Python
"""
