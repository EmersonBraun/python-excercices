from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = 'SELECT * FROM contacts'

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        for r in result:
            print(f'{r[2]:2d} - {r[0]:10s} Tel: {r[1]}')
