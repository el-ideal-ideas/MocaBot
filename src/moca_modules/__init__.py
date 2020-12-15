# -- Init --------------------------------------------------------------------------

from .moca_data.requirements import REQUIREMENTS

for __cnt in range(3):
    try:
        from .init import *
        break
    except (ImportError, ModuleNotFoundError) as __error:
        from subprocess import call as __call, CalledProcessError
        from sys import platform as __platform, executable as __executable
        from time import sleep as __sleep

        print(f'Missing required module. <{__error}>')
        print('Try to install dependencies for moca_modules.')

        try:
            if __platform == 'win32' or __platform == 'cygwin':
                REQUIREMENTS.remove('uvloop')  # uvloop don't supports windows.
                __call(
                    f"{__executable} -m pip install pip {' '.join(REQUIREMENTS)}"
                    f" --upgrade --no-cache-dir",
                    shell=True
                )
            else:
                __call(
                    f"{__executable} -m pip install pip {' '.join(REQUIREMENTS)}"
                    f" --upgrade --no-cache-dir",
                    shell=True
                )
            print('Installed dependencies for moca_modules successfully.')
            break
        except CalledProcessError as e:
            print(f'Install failed some error occurred. <CalledProcessError: {e}>')
            print('Try to install dependencies again in 5 seconds. Please wait.')
            __sleep(5)

# -------------------------------------------------------------------------- Init --
