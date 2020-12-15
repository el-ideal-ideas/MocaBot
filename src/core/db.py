# -- Imports --------------------------------------------------------------------------

from pymysql import Connection, MySQLError
from .core import DB_CONFIG
from .. import moca_modules as mzk

# -------------------------------------------------------------------------- Imports --

# -- DB --------------------------------------------------------------------------

try:
    mysql = Connection(
        host=DB_CONFIG['mysql']['host'],
        port=int(DB_CONFIG['mysql']['port']),
        user=DB_CONFIG['mysql']['user'],
        password=DB_CONFIG['mysql']['password'],
        database=DB_CONFIG['mysql']['database']
    )
    cursor = mysql.cursor()
except KeyError as e:
    mzk.print_error(f'Mysql database configuration error. missing key: {e}')
    mzk.sys_exit(1)
except MySQLError as e:
    mzk.print_error("Can't connect to MySQL database, Please check your database configuration.")
    mzk.print_error("And make sure your database is online.")
    mzk.print_error("You can use 'python3 moca.py test-mysql-con' to check your database.")
    mzk.print_error(f"<MySQLError: {e}>")
    mzk.sys_exit(1)

# -------------------------------------------------------------------------- DB --
