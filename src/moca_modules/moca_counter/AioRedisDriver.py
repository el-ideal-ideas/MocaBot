# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, Union, Tuple
)
from aioredis import create_pool, ConnectionsPool, RedisError
from ssl import SSLContext
from uuid import uuid4
from .AsyncDriverInterface import AsyncDriverInterface
from ..moca_core import ENCODING

# -------------------------------------------------------------------------- Imports --

# -- Async Redis Driver --------------------------------------------------------------------------


class AioRedisDriver(AsyncDriverInterface):
    """
    -- english --------------------------------------------------------------------------
    This is a async redis driver.
    At first you need run init_connection_pool method or set_connection_pool method.
    -- 日本語 --------------------------------------------------------------------------
    これは非同期Redisのドライバーです。
    使用する前にinit_connection_poolメソッドあるいは、set_connection_poolメソッドを実行する必要があります。
    -- 中文 --------------------------------------------------------------------------
    这是Redis的异步驱动。
    使用前您需要执行init_connection_pool方法或者set_connection_pool方法。

    Attributes
    ----------
    self._pool: Optional[ConnectionsPool]
        the connection pool of redis.

    self._encoding: str
        the character encoding of redis.

    self._prefix: str
        the prefix for data key.
    """

    NAME = 'AioRedisDriver'

    VERSION = '1.0.3'

    def __init__(
            self,
            pool: Optional[ConnectionsPool] = None,
            prefix: Optional[str] = None,
    ):
        """
        :param pool:  a async redis connection pool.
        :param prefix: the prefix for data key.
        """
        self._pool: Optional[ConnectionsPool] = pool
        self._encoding: str = ENCODING
        self._prefix: str = uuid4().hex if prefix is None else prefix

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def init_connection_pool(
            self,
            address: Union[Tuple[str, int], str],
            db: int,
            password: Optional[str] = None,
            ssl: Optional[SSLContext] = None,
            encoding: str = ENCODING,
            minsize: int = 1,
            maxsize: int = 10
    ) -> Tuple[bool, str]:
        """
        Create a connection pool.
        :param address: Tuple(ip-address, port)
        :param db: database name.
        :param password: your password
        :param ssl: the ssl context.
        :param encoding: the character encoding for response.
        :param minsize: minimum size of connection pool.
        :param maxsize: maximum size of connection pool.
        :return: Tuple(status, message)
        If initialized pool successfully, self._pool will be set to connection pool.
        If some error occurred. self._pool will be set to None.
        """
        try:
            self._pool = await create_pool(address,
                                           db=db,
                                           password=password,
                                           ssl=ssl,
                                           encoding=encoding,
                                           minsize=minsize,
                                           maxsize=maxsize)
            if self._encoding != encoding:
                self._encoding = encoding
            return True, 'success'
        except RedisError as error:
            self._pool = None
            return False, str(error)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set_connection_pool(self,
                            pool: ConnectionsPool) -> None:
        """
        Set the connection pool.
        :param pool: connection pool instance.
        :return: None
        """
        self._pool = pool

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set_encoding(self,
                     encoding: str) -> None:
        """
        Set character encoding.
        :param encoding: the character encoding for response.
        :return: None
        """
        self._encoding = encoding

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def pool(self) -> Optional[ConnectionsPool]:
        return self._pool

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def encoding(self) -> Optional[str]:
        return self._encoding

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def add(self,
                  key: str,
                  value: int = 1) -> Tuple[bool, Optional[int], str]:
        """
        Add count by key.
        :param key: the key of the counter.
        :param value: the value to add.
        :return: Tuple(status, count, message) If can't get the value of counter, count will be None.
        """
        if self._pool is None:
            return False, None, 'please initialize the connection pool'
        try:
            async with self._pool.get() as redis:
                result = await redis.execute('incrby', self._prefix + key, value, encoding=self._encoding)
            try:
                return True, int(result), 'success'
            except (ValueError, TypeError):
                return True, None, 'success'
        except RedisError as error:
            return False, None, str(error)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def set(self,
                  key: str,
                  value: int) -> Tuple[bool, str]:
        """
        Set count by key.
        :param key: the key of the counter.
        :param value: the value to set.
        :return: Tuple(status, message)
        """
        if self._pool is None:
            return False, 'please initialize the connection pool'
        try:
            async with self._pool.get() as redis:
                await redis.execute('set', self._prefix + key, value, encoding=self._encoding)
            return True, 'success'
        except RedisError as error:
            return False, str(error)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def get(self,
                  key: str,
                  default: Optional[int] = None) -> Tuple[Optional[int], str]:
        """
        Get the count by key.
        :param key: the key of the counter.
        :param default: the default value.
        :return: Tuple(value, message). if some error occurred, the response value will be default value.
        """
        if self._pool is None:
            return default, 'please initialize the connection pool'
        try:
            async with self._pool.get() as redis:
                result = await redis.execute('get', self._prefix + key, encoding=self._encoding)
            try:
                return int(result), 'success'
            except (ValueError, KeyError) as error:
                return None, str(error)
        except RedisError as error:
            return default, str(error)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    async def clear(self,
                    key: str) -> Tuple[bool, str]:
        """
        Clear the count by key.
        :param key: the key of the counter.
        :return: Tuple(status, message)
        """
        if self._pool is None:
            return False, 'please initialize the connection pool'
        try:
            async with self._pool.get() as redis:
                await redis.execute('del', self._prefix + key, encoding=self._encoding)
            return True, 'success'
        except RedisError as error:
            return False, str(error)

# -------------------------------------------------------------------------- Async Redis Driver --
