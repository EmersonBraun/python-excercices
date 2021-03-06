from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = 'INSERT INTO contacts(name, tel) VALUES (%s,  %s)'
args = ('Lucas', '9876-54321')

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        cursor.execute(sql, args)
        connection.commit()
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        print(f'Insert ID: {cursor.lastrowid}')
