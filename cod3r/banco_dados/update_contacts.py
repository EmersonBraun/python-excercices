from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = 'UPDATE contacts SET name = %s WHERE id = %s'

with new_connection() as connection:
    try:
        idc = input('Id Contacts to update: ')
        name = input('New name: ')
        args = (name, idc)
        cursor = connection.cursor()
        cursor.execute(sql, args)
        connection.commit()
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        print(f'{id} registry updated')
