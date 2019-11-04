from mysql.connector import connect
# from mysql.connector.errors import ProgrammingError
from contextlib import contextmanager

params = dict(
    host='localhost',
    port=3306,
    user='root',
    passwd='12345',
    database='agenda'
)


@contextmanager
def new_connection():
    connection = connect(**params)
    try:
        yield connection
    finally:
        if(connection and connection.is_connected()):
            connection.close()
            print('Connection closed')
