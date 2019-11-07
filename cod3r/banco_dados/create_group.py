from db import new_connection
from mysql.connector import ProgrammingError

table_group = """
    CREATE TABLE IF NOT EXISTS groups(
        id INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(40)
    )
"""

alter_contacts1 = """
    ALTER TABLE contacts ADD group_id INT
"""
alter_contacts2 = """
    ALTER TABLE contacts ADD FOREIGN KEY (group_id)
    REFERENCES groups(id)
"""

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        cursor.execute(table_group)
        cursor.execute(alter_contacts1)
        cursor.execute(alter_contacts2)
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
