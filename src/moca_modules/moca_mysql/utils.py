# -- Imports --------------------------------------------------------------------------

from typing import (
    Tuple
)
from pymysql import Connection
from pymysql.err import MySQLError

# -------------------------------------------------------------------------- Imports --

# -- Utils --------------------------------------------------------------------------


def test_mysql_connection(host: str, port: int, user: str, password: str, dbname: str) -> Tuple[bool, str]:
    """
    Test the database connection.
    :return: status, message.
    """
    try:
        con = Connection(host=host,
                         port=port,
                         user=user,
                         password=password,
                         db=dbname)
        con.ping()
        con.close()
        return True, 'success.'
    except MySQLError as e:
        return False, str(e).split(',')[1].strip()[1:-2]

# -------------------------------------------------------------------------- Utils --
