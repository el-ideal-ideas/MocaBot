# -- Imports --------------------------------------------------------------------------

from typing import (
    Dict, Callable, Union, Optional
)
from .schedule import Job, run_pending, CancelJob, every, ScheduleValueError, cancel_job
from time import sleep
from queue import Queue
from functools import wraps
from traceback import format_exc
from threading import Thread
from pathlib import Path
from ..moca_core import ENCODING, NEW_LINE

# -------------------------------------------------------------------------- Imports --

# -- MocaScheduler --------------------------------------------------------------------------


class MocaScheduler:
    """
    This is a simple scheduler module based on https://github.com/dbader/schedule

    Attributes
    ----------
    self._worker_thread: Thread
        the main worker thread.
    self._scheduler_loop_thread: Thread
        run the scheduler loop on other thread.
    self._job_queue: Queue
        the job queue.
    self.job_dict: Dict[str, Job]
        the dictionary of jobs.
    self._log_file: Optional[str]
        the path of the log file.
    self._log_encoding: str
        the text encoding of the log file.
    """

    def __init__(
            self,
            log_file: Optional[Union[str, Path]] = None,
            log_encoding: str = ENCODING,
    ):
        # set the log file.
        self._log_file: Optional[str] = str(log_file) if log_file is not None else None
        # set encoding
        self._log_encoding: str = log_encoding
        # set the job queue.
        self._job_queue: Queue = Queue()
        # set job dictionary.
        self.job_dict: Dict[str, Job] = {}
        # run worker thread.
        self._worker_thread: Thread = Thread(target=self._worker_main, daemon=True)
        self._worker_thread.start()
        # run scheduler event loop.
        self._scheduler_loop_thread: Thread = Thread(
            target=self._start_event_loop, name='Scheduler Loop Thread', daemon=True
        )
        self._scheduler_loop_thread.start()
        self._save_log('Started scheduler event loop by schedule module.')

    def _worker_main(self) -> None:
        """
        the worker for schedule module.
        """
        while True:
            job_func = self._job_queue.get()
            job_func()
            self._job_queue.task_done()

    @staticmethod
    def _start_event_loop() -> None:
        """
        start event loop
        """
        while True:
            run_pending()
            sleep(1)
            
    def _save_log(self, message: str) -> None:
        """Append the message to log file."""
        if self._log_file is not None:
            with open(self._log_file, mode='a', encoding=ENCODING) as file:
                file.write(message)
                file.write(NEW_LINE)

    def _save_add_event_success_log(self, name: str, time: str) -> None:
        self._save_log(f'Add a loop event success. name: {name}, time: {time}')

    def _save_add_event_failed_log(self, name: str, error: str) -> None:
        self._save_log(f'Add a loop event failed, name: {name}, error: {error}')

    def _save_add_timeout_event_success_log(self, name: str, time: str) -> None:
        self._save_log(f'Add a timeout event success. name: {name}, time: {time}')

    def _save_add_timeout_event_failed_log(self, name: str, error: str) -> None:
        self._save_log(f'Add a timeout event failed, name: {name}, error: {error}')

    def add_event_per_second(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        add loop event per second.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).seconds.do(self._job_queue.put, job)
            self._save_add_event_success_log(name, f'per {time} seconds.')
            return True
        else:
            self._save_add_event_failed_log(name, 'the name must be unique.')
            return False

    def add_event_per_minute(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        add loop event per minute.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).minutes.do(self._job_queue.put, job)
            self._save_add_event_success_log(name, f'per {time} minutes.')
            return True
        else:
            self._save_add_event_failed_log(name, 'the name must be unique.')
            return False

    def add_event_per_hour(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        add loop event per hour.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).hours.do(self._job_queue.put, job)
            self._save_add_event_success_log(name, f'per {time} hours.')
            return True
        else:
            self._save_add_event_failed_log(name, 'the name must be unique.')
            return False

    def add_event_per_day(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        add loop event per day.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).days.do(self._job_queue.put, job)
            self._save_add_event_success_log(name, f'per {time} days.')
            return True
        else:
            self._save_add_event_failed_log(name, 'the name must be unique.')
            return False

    def add_event_at_time_every_day(self, name: str, job: Callable, time: str) -> bool:
        """
        add a loop event at the time, and run the event every day.
        :param name: the job name
        :param job: the target job
        :param time: time to run event, the format sample "09:30".
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            try:
                self.job_dict[name] = every().day.at(time).do(self._job_queue.put, job)
                self._save_add_event_success_log(name, f'at every {time}.')
                return True
            except ScheduleValueError:
                self._save_add_event_failed_log(name, 'time format error.')
                return False
        else:
            self._save_add_event_failed_log(name, 'the name must be unique.')
            return False

    def _job_that_executes_once(self, func: Callable, name: str):
        """
        do job only once
        """
        del self.job_dict[name]
        self._job_queue.put(func)
        return CancelJob

    def run_event_with_timeout_second(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        run event with timeout use second.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).seconds.do(self._job_that_executes_once, job, name)
            self._save_add_timeout_event_success_log(name, f'run in {time} seconds.')
            return True
        else:
            self._save_add_timeout_event_failed_log(name, 'the name must be unique.')
            return False

    def run_event_with_timeout_minute(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        run event with timeout use minute.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).minutes.do(self._job_that_executes_once, job, name)
            self._save_add_timeout_event_success_log(name, f'run in {time} minutes.')
            return True
        else:
            self._save_add_timeout_event_failed_log(name, 'the name must be unique.')
            return False

    def run_event_with_timeout_hour(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        run event with timeout use hour.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).hours.do(self._job_that_executes_once, job, name)
            self._save_add_timeout_event_success_log(name, f'run in {time} hours.')
            return True
        else:
            self._save_add_timeout_event_failed_log(name, 'the name must be unique.')
            return False

    def run_event_with_timeout_day(self, name: str, job: Callable, time: int = 1) -> bool:
        """
        run event with timeout use day.
        :param name: event name
        :param job: event job
        :param time: event interval time
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            self.job_dict[name] = every(time).days.do(self._job_that_executes_once, job, name)
            self._save_add_timeout_event_success_log(name, f'run in {time} days.')
            return True
        else:
            self._save_add_timeout_event_failed_log(name, 'the name must be unique.')
            return False

    def add_event_at_time_execute_once(self, name: str, job: Callable, time: str) -> bool:
        """
        add a event at the time, and run the event once.
        :param name: the job name
        :param job: the target job
        :param time: time to run event, the format sample "09:30".
        :return: status, [success] or [failed]
        """
        if name not in self.job_dict:
            try:
                self.job_dict[name] = every().day.at(time).do(self._job_that_executes_once, job, name)
                self._save_add_timeout_event_success_log(name, f'run once at {time}.')
                return True
            except ScheduleValueError:
                self._save_add_timeout_event_failed_log(name, 'time format error.')
                return False
        else:
            self._save_add_timeout_event_failed_log(name, 'the name must be unique.')
            return False

    def remove_job(self, name: str) -> bool:
        """
        cancel the event.
        :param name: the name of event.
        :return: status, [success] or [failed]
        """
        if name in self.job_dict:
            cancel_job(self.job_dict[name])
            del self.job_dict[name]
            self._save_log(f'Remove loop event success. name: {name}')
            return True
        else:
            self._save_log(f'Remove loop event failed. error: unknown name.')
            return False

    @staticmethod
    def catch_exceptions(cancel_on_failure: bool = False,
                         print_exception: bool = False, 
                         log_file: Optional[Union[str, Path]] = None,
                         encoding: str = ENCODING):
        """
        this is a decorator, to catch exception in scheduled job.
        :param cancel_on_failure: if this param is true, when exception occurred, cancel job.
        :param print_exception: print the exception info to console.
        :param log_file: save the exception to file.
        :param encoding the encoding of the log file.
        """
        def catch_exceptions_decorator(job_func):
            @wraps(job_func)
            def wrapper(*args, **kwargs):
                try:
                    return job_func(*args, **kwargs)
                except Exception as e:
                    error = format_exc()
                    if print_exception:
                        print(error)
                    if log_file is not None:
                        with open(str(log_file), mode='a', encoding=encoding) as file:
                            file.write(f'<Exception: {e}> An error occurred when running {job_func.__name__}{NEW_LINE}')
                            file.write(error)
                    if cancel_on_failure:
                        return CancelJob

            return wrapper
        return catch_exceptions_decorator

    def with_logging(self):
        """
        this is a decorator, can logging the start and end of the job
        """
        def with_logging_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self._save_log(f'Running job: {func.__name__}.')
                result = func(*args, **kwargs)
                self._save_log(f'Job {func.__name__} completed.')
                return result

            return wrapper
        return with_logging_decorator
