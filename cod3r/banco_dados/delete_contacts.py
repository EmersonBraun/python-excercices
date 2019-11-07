from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = "DELETE FROM contacts WHERE name = %s"

with new_connection() as connection:
    try:
        name = input('Contacts to delete: ')
        args = (f'{name}',)
        cursor = connection.cursor()
        cursor.execute(sql, args)
        connection.commit()
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        print(f'{cursor.rowcount} registry deleteds')
