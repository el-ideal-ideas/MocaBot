# -- Imports --------------------------------------------------------------------------

from typing import (
    Callable, Dict, Optional, Union
)
from pathlib import Path
from multiprocessing import Process, Queue
from traceback import format_exc, print_exc
from concurrent.futures import ThreadPoolExecutor
from ..moca_utils import set_process_name, get_my_pid, get_random_string, print_info
from ..moca_core import ENCODING, NEW_LINE, IS_DEBUG

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

MAX_WORKERS: int = 16

# -------------------------------------------------------------------------- Variables --

# -- MocaPy --------------------------------------------------------------------------


class MocaPy:
    """
    Run python task in background process.

    Important!
        Please use this class under if __name__ == '__main__':

    Attributes
    ----------
    self._func_dict: Dict[str, Callable]
        this is a dictionary use the name as a key and the function as a value.
    self._queue: Queue
        this queue was used to send command to the background process.
    self._process: Optional[Process]
        the instance of the background process.
    self._error_log: str
        the file name of the error log.
    self._encoding: str
        the encoding of the error log.
    self._name: str
        the name of the background process.
    self._workers: int
        the number of the threads in the background process.
    """

    EXEC: str = '[el]#moca_exec#'
    DEBUG: str = '[el]#moca_debug#'

    def __init__(
            self,
            name: Optional[str] = None,
            error_log: Union[str, Path] = '',
            log_encoding: str = ENCODING,
            workers: int = MAX_WORKERS,
    ):
        self._name: str = name if name is not None else get_random_string(6)
        self._func_dict: Dict[str, Callable] = {}
        self._queue: Queue = Queue()
        self._process: Optional[Process] = None
        self._error_log: str = str(error_log)
        self._encoding: str = log_encoding
        self._workers: int = workers
        # check the log file.
        if error_log != '':
            with open(self._error_log, mode='a', encoding=self._encoding) as _:
                pass

    @property
    def process(self) -> Optional[Process]:
        return self._process

    @property
    def name(self) -> str:
        return self._name

    def register_function(self, func: Callable) -> None:
        """
        If you register the function with this method. You can use the `name(str)` of the function in `add_task` method.
        """
        self._func_dict[func.__name__] = func

    def add_task(self, func: Union[str, Callable], *args, **kwargs) -> None:
        """Run the task on the background process."""
        self._queue.put((func, args, kwargs))

    def add_python_script(self, script: str) -> None:
        self._queue.put((self.EXEC, script))
        
    def start_debug_mode(self) -> None:
        """Print errors on console."""
        self._queue.put((self.DEBUG,))

    @staticmethod
    def _task_loop(queue: Queue, func_dict: Dict[str, Callable], error_log: str, encoding: str, name: str) -> None:
        set_process_name(f'MocaPy Background Process ({name}) -- {get_my_pid()}')
        executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        debug_flag: bool = IS_DEBUG

        def __exception_handler(func: Callable, debug: bool, *args, **kwargs) -> None:
            try:
                func(*args, **kwargs)
            except Exception as e:
                if debug:
                    print_exc()
                if error_log != '':
                    with open(error_log, mode='a', encoding=encoding) as error_file:
                        error_file.write(
                            f'<Exception: {e}> Name: {func.__name__},'
                            f' Args: {str(args)},'
                            f' Kwargs: {str(kwargs)}{NEW_LINE}'
                        )
                        error_file.write(format_exc())
        try:
            while True:
                data = queue.get()
                if MocaPy.DEBUG in data:
                    debug_flag = True
                    print_info('<MocaPy> Debug mode is turned on.')
                elif data[0] == MocaPy.EXEC:
                    executor.submit(__exception_handler, exec, debug_flag, data[1])
                elif isinstance(data[0], str) and data[0] in func_dict:
                    executor.submit(__exception_handler, func_dict[data[0]], debug_flag, *data[1], **data[2])
                else:
                    executor.submit(__exception_handler, data[0], debug_flag, *data[1], **data[2])
        except (KeyboardInterrupt, SystemExit):
            pass

    def run_process(self) -> None:
        self._process = Process(target=self._task_loop,
                                args=(self._queue, self._func_dict, self._error_log, self._encoding, self._name),
                                daemon=True)
        self._process.start()

# -------------------------------------------------------------------------- MocaPy --
