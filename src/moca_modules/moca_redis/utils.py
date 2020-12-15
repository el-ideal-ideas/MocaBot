# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Tuple
)
from redis import Redis, RedisError
from uuid import uuid4

# -------------------------------------------------------------------------- Imports --

# -- Utils --------------------------------------------------------------------------


def test_redis_connection(host: str, port: int, password: Optional[str] = None) -> Tuple[bool, str]:
    try:
        con: Redis = Redis(host, port, 0, password)
        key = 'moca_modules_connection_test_key' + uuid4().hex
        con.set(key, 0)
        con.delete(key)
        con.close()
        return True, 'success'
    except RedisError as e:
        return False, str(e)


# -------------------------------------------------------------------------- Utils --
