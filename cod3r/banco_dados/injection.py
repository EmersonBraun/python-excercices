from db import new_connection
from mysql.connector import ProgrammingError


with new_connection() as connection:
    command = input('SQL: ')
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        print('Command executed')
