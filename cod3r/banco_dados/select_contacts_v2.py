from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = 'SELECT id, name FROM contacts'

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        for result in cursor.fetchall():
            print('\t'.join(str(field) for field in result))
