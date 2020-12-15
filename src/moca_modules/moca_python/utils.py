# -- Imports --------------------------------------------------------------------------

from typing import (
    Union
)
from pathlib import Path
from subprocess import call
from sys import executable
from ..moca_core import ENCODING, IS_UNIX_LIKE

# -------------------------------------------------------------------------- Imports --

# -- Utils --------------------------------------------------------------------------


def exec_python_file(filename: Union[str, Path], encoding: str = ENCODING) -> None:
    """
    execute a python script file.
    Important!
    Please only execute trusted files.
    """
    with open(str(filename), mode='r', encoding=encoding) as file:
        exec(file.read())


def run_python_file(filename: Union[str, Path], *args) -> None:
    """
    run a python program on background.
    Important!
    Please only execute trusted files.
    This function only supports unix like systems.
    """
    if IS_UNIX_LIKE:
        call(f'{executable} {str(filename)} {" ".join(args)}', shell=True)
    else:
        raise OSError('This function only supports unix like systems.')


# -------------------------------------------------------------------------- Utils --
