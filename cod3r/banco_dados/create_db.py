from config import connection

cursor = connection.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS agenda')
