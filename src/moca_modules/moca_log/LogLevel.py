# -- LogLevel --------------------------------------------------------------------------


DEBUG: int = 0
INFO: int = 1
WARNING: int = 2
ERROR: int = 3
CRITICAL: int = 4


class LogLevel(object):
    """The logging level for Moca Log Class."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    @classmethod
    def int_to_str(cls, integer: int) -> str:
        if integer == 0:
            return 'DEBUG'
        elif integer == 1:
            return 'INFO'
        elif integer == 2:
            return 'WARNING'
        elif integer == 3:
            return 'ERROR'
        elif integer == 4:
            return 'CRITICAL'
        else:
            raise ValueError('Invalid integer value, only 0, 1, 2, 3, 4')

    @classmethod
    def str_to_int(cls, string: str) -> int:
        if string == 'DEBUG':
            return 0
        elif string == 'INFO':
            return 1
        elif string == 'WARNING':
            return 2
        elif string == 'ERROR':
            return 3
        elif string == 'CRITICAL':
            return 4
        else:
            raise ValueError('Invalid string value, only DEBUG, INFO, WARNING, ERROR, CRITICAL')

# -------------------------------------------------------------------------- LogLevel --
