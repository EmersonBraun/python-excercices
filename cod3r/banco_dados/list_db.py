from config import connection

cursor = connection.cursor()
cursor.execute('SHOW DATABASES')

for i, database in enumerate(cursor, start=1):
    print(f'DB {i}: {database[0]}')
