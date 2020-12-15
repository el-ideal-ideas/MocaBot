# -- MocaMultiProcessLock --------------------------------------------------------------------------

class MocaMultiProcessLock:
    __slots__ = ("_rlock", "_blocking", "_acquired")

    def __init__(self, rlock, blocking):
        self._rlock = rlock
        self._blocking = blocking
        self._acquired = False

    @property
    def acquired(self):
        return self._acquired

    def __enter__(self):
        self._acquired = self._rlock.acquire(blocking=self._blocking)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._acquired:
            self._rlock.release()

# -------------------------------------------------------------------------- MocaMultiProcessLock --
