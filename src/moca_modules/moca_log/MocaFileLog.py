# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Union
)
from pathlib import Path
from queue import Queue
from datetime import datetime
from traceback import format_exc, print_exc
from ..moca_core import tz, ENCODING, NEW_LINE
from ..moca_file import MocaFileAppendController
from ..moca_utils import (
    location, get_my_pid, get_my_tid, print_debug, print_info, print_warning, print_error, print_critical
)
from .LogLevel import LogLevel

# -------------------------------------------------------------------------- Imports --

# -- MocaFileLog --------------------------------------------------------------------------


class MocaFileLog(MocaFileAppendController):
    """
    This class will put logs into queue, and append logs to the file in other thread,
    to return the response more quickly.
    ログメッセージをキューに入れて、別スレッドで追記処理を行うことで、レスポンスを返す速度を速める。
    把日志信息放进列队里面，然后在别的线程内进行文件的IO处理，提高程序的体感速度。

    Attributes
    ----------
    self._queue: Queue
        the task queue.
    self._filename: str
        The path of target file.
    self._encoding: str
        The encoding of the target file.
    self._log_level: int
        The log level of this instance.
    self._pid: Optional[int]
        The process id of this process.
    self._debug: bool
        The flag of debug mode.
    """

    def __init__(
            self,
            filename: Union[str, Path],
            log_level: int = 1,
            encoding: str = ENCODING,
            queue: Optional[Queue] = None,
            maxsize: int = 0
    ):
        """
        :param filename: The path of target file.
        :param log_level: The log level of this instance.
        :param encoding: The encoding of the target file.
        :param queue: a instance of Queue class.
        :param maxsize: the maximum size of the queue, If maxsize is <= 0, the queue size is infinite.
        """
        super().__init__(filename=filename, encoding=encoding, queue=queue, maxsize=maxsize)
        self._log_level: int = log_level
        self._pid: Optional[int] = get_my_pid()
        self._debug: bool = False

    @property
    def log_level(self) -> int:
        return self._log_level

    def set_log_level(self, level: int) -> bool:
        """Change the log level."""
        if level in (0, 1, 2, 3, 4):
            self._log_level = level
            return True
        else:
            return False

    def write_log(self, message: str, level: int) -> None:
        """
        Add a log message into the queue.
        :param message: the log message.
        :param level: the log level.
        :return: None
        Log Format
        ----------
        [loglevel](time)<filename|caller|line number|process id|thread id> message
        """
        if self._log_level <= level:
            filename, caller, line = location()
            current_time = datetime.now(tz=tz)
            msg = f"[{LogLevel.int_to_str(level)}]({str(current_time)})" \
                  f"<{filename}|{caller}|{line}|{self._pid or 0}|{get_my_tid()}>" \
                  f"{message}{NEW_LINE}"
            self.write(msg)
            if self._debug:
                self._print_log(msg, level)
        else:
            pass  # do nothing

    def write_exception(self) -> None:
        msg = "-- Exception -------------------------------------" \
              f"{format_exc()}" \
              f"------------------------------------- Exception --{NEW_LINE}"
        self.write(msg)
        if self._debug:
            print("-- Exception -------------------------------------")
            print_exc()
            print("------------------------------------- Exception --")
        
    def start_dev_mode(self) -> None:
        """Show all logs on the console."""
        self._debug = True
        
    def stop_dev_mode(self) -> None:
        """Stop development mode."""
        self._debug = False
        
    def print_log(self, message: str, level: int) -> None:
        """Print a log message."""
        if self._log_level <= level:
            filename, caller, line = location()
            current_time = datetime.now(tz=tz)
            msg = f"[{LogLevel.int_to_str(level)}]({str(current_time)})" \
                  f"<{filename}|{caller}|{line}|{self._pid or 0}|{get_my_tid()}>" \
                  f"{message}"
            self._print_log(msg, level)
        else:
            pass  # do nothing
    
    @staticmethod
    def _print_log(message: str, level: int) -> None:
        """Print message with color."""
        if level == LogLevel.DEBUG:
            print_debug(message)
        elif level == LogLevel.INFO:
            print_info(message)
        elif level == LogLevel.WARNING:
            print_warning(message)
        elif level == LogLevel.ERROR:
            print_error(message)
        elif level == LogLevel.CRITICAL:
            print_critical(message)

    def clear_log(self) -> None:
        self.write(self.CLEAR_CMD)

    def get_all_log(self) -> str:
        with open(self._filename, mode='r', encoding=self._encoding) as file:
            return file.read()
        
# -------------------------------------------------------------------------- MocaFileLog --
