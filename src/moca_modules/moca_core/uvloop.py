# -- Functions --------------------------------------------------------------------------


def is_uvloop() -> bool:
    """If system is using uvloop, return True"""
    try:
        from uvloop import EventLoopPolicy
        from asyncio import get_event_loop_policy
        return isinstance(get_event_loop_policy(), EventLoopPolicy)
    except (ImportError, ModuleNotFoundError):
        return False


def try_setup_uvloop() -> bool:
    """
    If uvloop module is installed, use uvloop as the default event loop.
    If setup uvloop success, return True.
    """
    try:
        from uvloop import EventLoopPolicy, install
        from asyncio import get_event_loop_policy
        if not isinstance(get_event_loop_policy(), EventLoopPolicy):
            install()
        return True
    except (ImportError, ModuleNotFoundError):
        return False

# -------------------------------------------------------------------------- Functions --
