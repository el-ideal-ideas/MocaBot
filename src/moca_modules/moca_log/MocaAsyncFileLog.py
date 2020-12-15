# -- Import --------------------------------------------------------------------------

from typing import (
    Optional, Union
)
from aiofiles import open as aio_open
from pathlib import Path
from traceback import format_exc, print_exc
from datetime import datetime
from .LogLevel import LogLevel
from ..moca_core import tz, ENCODING, NEW_LINE
from ..moca_utils import (
    get_my_pid, get_my_tid, location, print_debug, print_info, print_warning, print_error, print_critical
)

# -------------------------------------------------------------------------- Import --

# -- MocaAsyncFileLog --------------------------------------------------------------------------


class MocaAsyncFileLog:
    """
    This class can write logs use asyncio.
    ログの非同期書き込み用クラス。
    异步化处理日志文件。

    Attributes
    ----------
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
    self._file
        The file object of log file.
    """

    def __init__(
            self,
            filename: Union[str, Path],
            log_level: int = 1,
            encoding: str = ENCODING,
    ):
        """
        :param filename: The path of target file.
        :param log_level: The log level of this instance.
        :param encoding: The encoding of the target file.
        """
        self._filename: str = str(filename)
        self._encoding: str = encoding
        self._log_level: int = log_level
        self._pid: Optional[int] = get_my_pid()
        self._debug: bool = False
        self._file = None

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

    async def write_log(self, message: str, level: int) -> None:
        """
        Add a log message into the queue.
        :param message: the log message.
        :param level: the log level.
        :return: None
        Log Format
        ----------
        [loglevel](time)<filename|caller|line number|process id|thread id> message
        """
        if self._file is None:
            self._file = await aio_open(self._filename, mode='a', encoding=self._encoding)
        if self._log_level <= level:
            filename, caller, line = location()
            current_time = datetime.now(tz=tz)
            msg = f"[{LogLevel.int_to_str(level)}]({str(current_time)})" \
                  f"<{filename}|{caller}|{line}|{self._pid or 0}|{get_my_tid()}>" \
                  f"{message}{NEW_LINE}"
            if self._file is not None:  # to pass mypy check
                await self._file.write(msg)
                await self._file.flush()
            if self._debug:
                self._print_log(msg, level)
        else:
            pass  # do nothing

    async def write_exception(self) -> None:
        msg = "-- Exception -------------------------------------" \
              f"{format_exc()}" \
              f"------------------------------------- Exception --{NEW_LINE}"
        if self._file is None:
            self._file = await aio_open(self._filename, mode='a', encoding=self._encoding)
        if self._file is not None:  # to pass mypy check
            await self._file.write(msg)
            await self._file.flush()
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

    async def clear_log(self) -> None:
        if self._file is not None:
            await self._file.close()
            Path(self._filename).unlink(missing_ok=True)
            self._file = await aio_open(self._filename, mode='a', encoding=self._encoding)

    async def get_all_log(self) -> str:
        async with aio_open(self._filename, mode='r', encoding=self._encoding) as file:
            return await file.read()

# -------------------------------------------------------------------------- MocaAsyncFileLog --
