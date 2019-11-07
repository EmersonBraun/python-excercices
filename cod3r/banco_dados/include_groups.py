from mysql.connector.errors import ProgrammingError
from db import new_connection

sql = 'INSERT INTO groups(descricao) VALUES (%s)'
args = (
    ('Casa', ),
    ('Trabalho',),
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
