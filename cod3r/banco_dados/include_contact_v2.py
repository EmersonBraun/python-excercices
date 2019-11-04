from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = 'INSERT INTO contacts(name, tel) VALUES (%s,  %s)'
args = (
    ('Lucas', '9876-54321'),
    ('Zé', '8876-54321'),
    ('Maria', '7876-54321'),
    ('João', '6876-54321'),
    ('ana', '5876-54321'),
)

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        cursor.executemany(sql, args)
        connection.commit()
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        print(f'Insert {cursor.rowcount} registry')
