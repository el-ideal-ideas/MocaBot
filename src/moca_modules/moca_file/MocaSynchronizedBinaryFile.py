# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Any
)
from pathlib import Path
from time import sleep
from threading import Thread
from .utils import get_timestamp

# -------------------------------------------------------------------------- Imports --

# -- MocaSynchronizedBinaryFile --------------------------------------------------------------------------


class MocaSynchronizedBinaryFile:
    """
    This class will synchronize with the target file.
    指定ファイルとメモリ上のデータを同期させる。
    让指定文件和内存上的数据同步。

    Attributes
    ----------
    self._filename: Path
        the path of target file.
    self._interval: float
        the interval to check update.
    self._file_content: bytes
        the file content.
    self._file_update_time: float
        the last modification time of the target file.
    self._thread: Thread
        a thread used to check file update.
    self._exit_thread: bool
        if this flag is True, the self._thread will stop.
    """

    def __init__(
            self,
            filename: Union[str, Path],
            check_interval: float = 0.1,
            manual_reload: bool = False,
    ):
        """
        :param filename: the file name of the target file.
        :param check_interval: the interval to check file (seconds).
        :param manual_reload: don't create the reload timer thread. You need run reload_file method manually.
        """
        # set filename
        self._filename: Path = Path(filename)
        # set check interval
        self._interval: float = check_interval
        # keep the file content on memory
        self._file_content: bytes
        try:
            with open(str(self._filename), mode='rb') as file:
                self._file_content = file.read()
        except FileNotFoundError:
            with open(str(self._filename), mode='wb') as _:
                pass  # create a new file
            self._file_content = ''.encode()
        self._file_update_time: float = get_timestamp(self._filename)
        # exit thread flag
        self._exit_thread: bool = False

        if not manual_reload:
            # file check loop
            def check_loop(self_: MocaSynchronizedBinaryFile):
                while True:
                    if self_._exit_thread:  # check exit thread flag
                        break
                    self_.reload_file()
                    sleep(self_._interval)

            self._thread: Thread = Thread(target=check_loop, args=(self,), daemon=True)
            self._thread.start()

    def __str__(self) -> str:
        return f'MocaSynchronizedBinaryFile: {self._filename}'

    def __del__(self):
        self._exit_thread = True
        try:
            self._thread.join()
        except AttributeError:
            pass

    @property
    def filename(self) -> Path:
        return self._filename

    @property
    def check_interval(self) -> float:
        return self._interval

    @property
    def file_content(self) -> bytes:
        return self._file_content

    def change_content(self, new_content: bytes) -> bytes:
        """Change the content of the file."""
        self._file_content = new_content
        with open(str(self._filename), mode='wb') as file:
            file.write(new_content)
        return self._file_content

    def append(self, data: bytes) -> bytes:
        """Appends text to the file."""
        self.change_content(self._file_content + data)
        return self._file_content

    def add_to_top(self, data: bytes) -> bytes:
        """Adds text to the top of the file."""
        self.change_content(data + self._file_content)
        return self._file_content

    def update_file(self) -> bytes:
        """save content to the file."""
        with open(str(self._filename), mode='wb') as file:
            file.write(self._file_content)
        return self._file_content

    def reload_file(self) -> bytes:
        """Reload the file manually."""
        time = get_timestamp(self._filename)
        if time != self._file_update_time:
            old = self._file_content
            with open(str(self._filename), mode='rb') as file:
                self._file_content = file.read()
            self._file_update_time = time
            self.reload_handler(self._file_content, old)
        return self._file_content
    
    def reload_handler(self, new_content: str, old_content: str) -> Any:
        """
        this function will be called when the file content was reloaded.
        You can override this method, to set a handler.
        """
        pass

    def clear_file(self) -> bytes:
        """Clear the content."""
        self.change_content(''.encode())
        return self._file_content

    def remove_file(self) -> None:
        """Remove the file."""
        self._exit_thread = True
        self._filename.unlink()

# -------------------------------------------------------------------------- MocaSynchronizedBinaryFile --
