# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Optional
)
from pathlib import Path
from threading import Thread
from queue import Queue
from ..moca_core import ENCODING

# -------------------------------------------------------------------------- Imports --

# -- MocaFileAppendController --------------------------------------------------------------------------


class MocaFileAppendController:
    """
    This class will put data into queue, and append data to the file in other thread,
    to return the response more quickly.
    データをキューに入れて、別スレッドで追記処理を行うことで、レスポンスを返す速度を速める。
    把数据放进列队里面，然后在别的线程内进行文件的IO处理，提高程序的体感速度。

    Attributes
    ----------
    self._queue: Queue
        the task queue.
    self._filename: str
        The path of target file.
    self._encoding: str
        The encoding of the target file.
    """

    CLEAR_CMD: str = '[el]#moca_clear#'  # If you put this message in the queue, The file will be cleared.

    def __init__(
            self,
            filename: Union[str, Path],
            encoding: str = ENCODING,
            queue: Optional[Queue] = None,
            maxsize: int = 0
    ):
        """
        :param filename: The path of target file.
        :param encoding: The encoding of the target file.
        :param queue: a instance of Queue class.
        :param maxsize: the maximum size of the queue, If maxsize is <= 0, the queue size is infinite.
        """
        # set queue
        self._queue: Queue = queue if queue is not None else Queue(maxsize=maxsize)
        # set filename
        self._filename: str = str(filename)
        # set encoding
        self._encoding: str = encoding
        # start the loop thread.
        Thread(
            target=MocaFileAppendController._write_loop,
            args=(self._queue, self._filename, self._encoding),
            daemon=True
        ).start()

    def __str__(self) -> str:
        return f'MocaFileAppendController: {self._filename}'

    @property
    def filename(self) -> str:
        return self._filename

    @staticmethod
    def _write_loop(queue: Queue, filename: str, encoding: str) -> None:
        file = open(filename, mode='a', encoding=encoding)
        while True:
            text = queue.get()
            if text == MocaFileAppendController.CLEAR_CMD:
                file.close()
                Path(filename).unlink(missing_ok=True)
                file = open(filename, mode='a', encoding=encoding)
            else:
                try:
                    file.write(text)
                    file.flush()
                except (PermissionError, OSError):
                    pass

    def write(self, text: str) -> None:
        """Add the text to the queue."""
        self._queue.put(text)

    @property
    def size(self) -> int:
        return self._queue.qsize()

# -------------------------------------------------------------------------- MocaFileAppendController --
