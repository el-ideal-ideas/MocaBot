"""
Welcome to Moca Commands.
"""

from sys import argv, executable
from subprocess import call
from pathlib import Path

if argv == ['moca.py', 'init']:
    call(f'{executable} -m pip install pip --upgrade', shell=True)
    call(
        f'{executable} -m pip install --upgrade -r '
        f'{str(Path(__file__).parent.joinpath("requirements.txt"))}',
        shell=True
    )
else:
    from src import moca_modules as mzk
    from src import console
    from src import core
    try:
        console()
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as error:
        mzk.print_critical(str(error))
        mzk.print_exc()
        mzk.append_str_to_file(core.LOG_DIR.joinpath('critical.log'), str(error))
        mzk.append_str_to_file(core.LOG_DIR.joinpath('critical.log'), mzk.format_exc())
