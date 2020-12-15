# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Any, List, Tuple
)
from time import sleep
from mmap import mmap
from pathlib import Path
try:
    from cloudpickle import dumps as p_dumps, loads as p_loads
except (ImportError, ModuleNotFoundError):
    from pickle import dumps as p_dumps, loads as p_loads

# -------------------------------------------------------------------------- Imports --

# -- MocaMMAPQ --------------------------------------------------------------------------


class MocaMMAPQ:
    """
    This is a MMAP based queue implementation.
    You can send data to another process, and receive data from another process.

    self._filename: Tuple[str, str]
        this file will be passed to mmap module.
    self._block_size: int
        system will send one block at once. If the data is too large the data will be split. (byte)
    self._sender_file
        a file object for sender.
    self._sender
        a mmap object for sender.
    self._receiver_file
        a file object for receiver.
    self._receiver
        a mmap object for receiver.
    """

    EOF = b'[el]#moca_mmapq_eof#'
    EOF_LEN = len(EOF)

    def __init__(
            self,
            sender: Union[str, Path],
            receiver: Union[str, Path],
            block_size: int = 520,
    ):
        """
        :param sender: this file will be passed to mmap module.
        :param receiver: this file will be passed to mmap module.
        :param block_size: system will send one block at once. If the data is too large the data will be split. (byte)
        """
        self._filename: Tuple[str, str] = (str(sender), str(receiver))
        self._block_size: int = block_size
        self._sender_file = open(self._filename[0], mode='w+b')
        self._sender_file.write(b'0' * (self._block_size + 1))
        self._sender_file.flush()
        self._sender = mmap(self._sender_file.fileno(), 0)
        self._receiver_file = open(self._filename[1], mode='w+b')
        self._receiver_file.write(b'0' * (self._block_size + 1))
        self._receiver_file.flush()
        self._receiver = mmap(self._receiver_file.fileno(), 0)

    @property
    def filename(self) -> Tuple[str, str]:
        return self._filename

    @property
    def block_size(self) -> int:
        return self._block_size

    def _send_wait(self, status: bytes) -> None:
        while True:
            if self._sender[0:1] == status:
                break
            else:
                sleep(0.001)

    def _receive_wait(self, status: bytes) -> None:
        while True:
            if self._receiver[0:1] == status:
                break
            else:
                sleep(0.001)

    def send(self, data: Any) -> None:
        """Send a data to another process."""
        pickled_data = p_dumps(data) + self.EOF
        size = len(pickled_data)
        if size > self._block_size:
            for i in range(size // self._block_size):
                index = i * self._block_size
                self._send_wait(b'0')
                self._sender[1:] = pickled_data[index: index + self._block_size]
                self._sender[0:1] = b'1'
            self._send_wait(b'0')
            self._sender[1:size - (index + self._block_size)] = pickled_data[index + self._block_size:]
            self._sender[0:1] = b'1'
        else:
            self._send_wait(b'0')
            self._sender[1:size+1] = pickled_data
            self._sender[0:1] = b'1'

    def receive(self) -> Any:
        """Receive a data from another process."""
        tmp: List[bytes] = []
        while True:
            self._receive_wait(b'1')
            res = self._receiver[1:]
            self._receiver[0:1] = b'0'
            if self.EOF in res:
                tmp.append(res[:res.index(self.EOF)])
                break
            else:
                tmp.append(res)
        pickled_data = b''.join(tmp)
        return p_loads(pickled_data)

# -------------------------------------------------------------------------- MocaMMAPQ --
