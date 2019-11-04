from db import new_connection
from mysql.connector import ProgrammingError

table_contacts = """
    CREATE TABLE IF NOT EXISTS contacts(
        name VARCHAR(50),
        tel VARCHAR(40)
    )
"""
table_emails = """
    CREATE TABLE IF NOT EXISTS emails(
        id INT AUTO_INCREMENT PRIMARY KEY,
        dono VARCHAR(50)
    )
"""

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        cursor.execute(table_contacts)
        cursor.execute(table_emails)
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
