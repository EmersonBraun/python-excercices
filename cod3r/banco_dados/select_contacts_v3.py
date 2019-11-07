from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = "SELECT * FROM contacts WHERE name like %s"

with new_connection() as connection:
    try:
        name = input('Contact to search: ')
        args = (f'%{name}%',)
        cursor = connection.cursor()
        cursor.execute(sql, args)
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        for result in cursor:
            print(result)
