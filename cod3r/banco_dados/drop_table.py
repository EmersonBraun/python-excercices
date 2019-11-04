from db import new_connection
from mysql.connector import ProgrammingError

table_contacts = """
    DROP TABLE IF EXISTS contacts
"""
table_emails = """
    DROP TABLE IF EXISTS emails
"""

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        cursor.execute(table_contacts)
        cursor.execute(table_emails)
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
