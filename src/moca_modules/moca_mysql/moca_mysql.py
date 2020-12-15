# -- Imports --------------------------------------------------------------------------

from typing import (
    Tuple, Optional
)
from pymysql import Connection
from pymysql.err import MySQLError, InternalError
from aiomysql import connect, create_pool
from time import time

# -------------------------------------------------------------------------- Imports --

# -- Moca Mysql --------------------------------------------------------------------------


class MocaMysql:
    """
    mysql database.

    Attributes
    ----------
    _host: str
        database host ip.
    _port: int
        database port number.
    _user: str
        database user name.
    _password: str
        database password.
    _dbname: str
        database name.
    _min: int
        the minimum size of the connection pool.
    _max: int
        the maximum size of the connection pool.
    _con
        a database connection.
    _aio_con
        a async database connection.
    _aio_pool
        a async database connection pool.
    self.force_sync: bool
        if _force_sync is True, use execute instead of execute_aio
    """

    _TEST_TABLE = """
    create table moca_test_table(
        id bigint auto_increment primary key,
        i int not null,
        j varchar(32) not null,
        k varchar(64) not null,
        l datetime not null
    ) ENGINE=InnoDB default charset = UTF8MB4;
    """

    _DROP_TEST_TABLE = "drop table moca_test_table;"

    _WRITE_TO_TEST_TABLE = "insert into moca_test_table(i,j,k,l) values(9, 'もちもち', 'にゃんにゃん', now());"

    _SELECT_FROM_TEST_TABLE = """select * from moca_test_table where id = 1;"""

    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
            dbname: str,
            minsize: int = 1,
            maxsize: int = 10):
        """
        :param host: database host ip.
        :param port: database port number.
        :param user: database user name.
        :param password: database password.
        :param dbname: database name.
        :param minsize: the minimum size of the connection pool.
        :param maxsize: the maximum size of the connection pool.
        """
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._dbname: str = dbname
        self._min: int = minsize
        self._max: int = maxsize
        self._con = Connection(host=host,
                               port=port,
                               user=user,
                               password=password,
                               db=dbname)
        self._aio_con = None
        self._aio_pool = None
        self.force_sync: bool = False

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def user(self) -> str:
        return self._user

    @property
    def dbname(self) -> str:
        return self._dbname

    def get_con(self):
        """Get a connection."""
        return self._con

    def get_a_con(self):
        """Get a con."""
        return self._con

    def get_a_new_con(self):
        """Get a new connection."""
        return Connection(host=self._host,
                          port=self._port,
                          user=self._user,
                          password=self._password,
                          db=self._dbname)

    async def get_a_aio_con(self):
        """Get a async connection."""
        if self._aio_con is None:
            con = await connect(host=self._host,
                                port=self._port,
                                user=self._user,
                                password=self._password,
                                db=self._dbname)
            self._aio_con = con
        else:
            con = self._aio_con
        return con

    async def get_a_new_aio_con(self):
        """Get a new async connection."""
        return await connect(host=self._host,
                             port=self._port,
                             user=self._user,
                             password=self._password,
                             db=self._dbname)

    async def get_a_aio_pool(self):
        """Get a async connection pool."""
        if self._aio_pool is None:
            pool = await create_pool(host=self._host,
                                     port=self._port,
                                     user=self._user,
                                     password=self._password,
                                     db=self._dbname,
                                     minsize=self._min,
                                     maxsize=self._max)
            self._aio_pool = pool
        else:
            pool = self._aio_pool
        return pool

    async def get_a_new_aio_pool(self):
        """Get a new async connection pool."""
        return await create_pool(host=self._host,
                                 port=self._port,
                                 user=self._user,
                                 password=self._password,
                                 db=self._dbname,
                                 minsize=self._min,
                                 maxsize=self._max)

    def execute(self, query: str, param: Tuple = (), commit: bool = False) -> Optional[Tuple]:
        """Execute the query."""
        con = self.get_con()
        cursor = con.cursor()
        cursor.execute(query, args=param)
        if commit:
            con.commit()
        try:
            return cursor.fetchall()
        except MySQLError:
            return None

    async def execute_aio(self, query: str, param: Tuple = (), commit: bool = False) -> Optional[Tuple]:
        """Execute the query."""
        if self.force_sync:
            return self.execute(query, param, commit)
        pool = await self.get_a_aio_pool()
        async with pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(query, args=param)
                data = await cur.fetchall()
                if commit:
                    await con.commit()
                return data if data != [] else None

    def create_test_table(self) -> None:
        """Create a test table."""
        try:
            self.execute(self._TEST_TABLE, commit=True)
        except InternalError:  # If table already exists.
            pass

    def drop_test_table(self) -> None:
        """Drop the test table."""
        try:
            self.execute(self._DROP_TEST_TABLE, commit=True)
        except InternalError:  # If table not exists.
            pass

    async def test_db_write_aio(self, count: int = 1000) -> float:
        """Write a data `count` times and return the spent time (seconds)."""
        s = time()
        for _ in range(count):
            await self.execute_aio(self._WRITE_TO_TEST_TABLE, commit=True)
        return time() - s

    def test_db_write(self, count: int = 1000) -> float:
        """Write a data `count` times and return the spent time (seconds)."""
        s = time()
        for _ in range(count):
            self.execute(self._WRITE_TO_TEST_TABLE, commit=True)
        return time() - s

    async def test_db_read_aio(self, count: int = 1000) -> float:
        """Write a data `count` times and return the spent time (seconds)."""
        s = time()
        for _ in range(count):
            await self.execute_aio(self._SELECT_FROM_TEST_TABLE)
        return time() - s

    def test_db_read(self, count: int = 1000) -> float:
        """Write a data `count` times and return the spent time (seconds)."""
        s = time()
        for _ in range(count):
            self.execute(self._SELECT_FROM_TEST_TABLE)
        return time() - s

# -------------------------------------------------------------------------- Moca Mysql --
