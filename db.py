import pymysql
from pymysql.cursors import DictCursor

def get_db_connection():
    """Return a new connection to the MySQL database.
Adjust the credentials if necessary."""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="fabrik",
        cursorclass=DictCursor,
        autocommit=True
    )
