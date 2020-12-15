# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Optional
)
from pathlib import Path
from threading import Thread
from queue import Queue
from ..moca_core import ENCODING
from ..moca_encrypt import MocaAES

# -------------------------------------------------------------------------- Imports --

# -- MocaWriteFileController --------------------------------------------------------------------------


class MocaWriteFileController:
    """
    This class will manage files, put data into queue, and write data in other thread.
    データをキューに入れて、別スレッドで書き込み処理を行うことで、レスポンスを返す速度を速める。
    把数据放进列队里面，然后在别的线程内进行文件的IO处理，提高程序的体感速度。

    Attributes
    ----------
    self._queue: Queue
        the task queue.
    """

    DEL_CMD: str = '[el]#moca_delete#'  # If you put this message in the queue, The file will be cleared.

    def __init__(
            self,
            queue: Optional[Queue] = None,
            maxsize: int = 0
    ):
        """
        :param queue: a instance of Queue class.
        :param maxsize: the maximum size of the queue, If maxsize is <= 0, the queue size is infinite.
        """
        # set queue
        self._queue: Queue = queue if queue is not None else Queue(maxsize=maxsize)
        # start the loop thread.
        Thread(target=MocaWriteFileController._write_loop, args=(self._queue,), daemon=True).start()

    def __str__(self) -> str:
        return 'MocaWriteFileController'

    @staticmethod
    def _write_loop(queue: Queue) -> None:
        file = None
        latest_name = None
        latest_encoding = None
        latest_mode = None
        while True:
            filename, mode, encoding, data = queue.get()
            if data == MocaWriteFileController.DEL_CMD:
                if file is not None and file.name == filename:
                    file.close()
                    file = None
                Path(filename).unlink(missing_ok=True)
            else:
                try:
                    if filename != latest_name or encoding != latest_encoding or mode != latest_mode:
                        if file is not None:
                            file.close()
                        file = open(filename, mode=mode, encoding=encoding)
                        latest_name = filename
                        latest_encoding = encoding
                        latest_mode = mode
                    if file is not None:
                        file.write(data)
                        file.flush()
                except (PermissionError, OSError):
                    pass

    def write(self, filename: Union[str, Path], mode: str, data: Union[bytes, str], encoding: str = ENCODING) -> None:
        """
        Write data into the file on other thread.
        Important!
            This method only supports mode=wb or mode=w or mode=a
        """
        if mode in ('wb', 'w', 'a'):
            self._queue.put((str(filename), mode, encoding, data))
        else:
            raise ValueError('This method only supports mode=wb or mode=w or mode=a')

    @property
    def size(self) -> int:
        return self._queue.qsize()

# -------------------------------------------------------------------------- MocaWriteFileController --

# -- MocaWriteEncryptedFileController --------------------------------------------------------------------------


class MocaWriteEncryptedFileController(MocaWriteFileController, MocaAES):
    """
    Add encryption to MocaWriteFileController class.

    Attributes
    ----------
    self._queue: Queue
        the task queue.
    self._aes: MocaAES
        an AES encryption module.
    self._mode: int
        the encryption mode.
        MODE_ECB = 1
        MODE_CBC = 2
        MODE_CFB = 3
        MODE_OFB = 5
        MODE_CTR = 6
        MODE_OPENPGP = 7
        MODE_CCM = 8
        MODE_EAX = 9
        MODE_SIV = 10
        MODE_GCM = 11
        MODE_OCB = 12
    """

    def __init__(
            self,
            password: Union[str, bytes],
            mode: int = 9,
            queue: Optional[Queue] = None,
            maxsize: int = 0
    ):
        """
        :param password: the password used to encrypt the file.
        :param mode: the encryption mode.
        :param queue: a instance of Queue class.
        :param maxsize: the maximum size of the queue, If maxsize is <= 0, the queue size is infinite.
        """
        MocaWriteFileController.__init__(self, queue, maxsize)
        MocaAES.__init__(self, password)
        # set aes object.
        self._aes: MocaAES = MocaAES(password)
        self._mode: int = mode

    def write(self, filename: Union[str, Path], mode: str, data: Union[bytes, str], encoding: str = ENCODING) -> None:
        """
        Write data into the file on other thread.
        Important!
            This method only supports mode=wb or mode=w
        """
        if mode in ('wb', 'w'):
            super(MocaWriteEncryptedFileController, self).write(
                filename,
                mode,
                self._aes.encrypt_string(data, self._mode)
                if isinstance(data, str)
                else self._aes.encrypt(data, self._mode),
                encoding
            )
        else:
            raise ValueError('This method only supports mode=wb or mode=w')

# -------------------------------------------------------------------------- MocaWriteEncryptedFileController --
