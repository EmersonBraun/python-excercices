from mysql.connector.errors import ProgrammingError
from db import new_connection

select_group = 'SELECT id FROM groups WHERE descricao = %s'
update_contact = 'UPDATE contacts SET group_id = %s WHERE name = %s'
contact_group = {
    'Lucas': 'Trabalho',
    'Lucas': 'Casa',
    'Lucas': 'Trabalho',
    'Lucas': 'Casa',
    'Lucas': 'Trabalho',
    'Lucas': 'Casa',
}

with new_connection() as connection:
    try:
        cursor = connection.cursor()
        for contato, group in contact_group.items():
            cursor.execute(select_group, (group,))
            group_id = cursor.fetchone()[0]
            cursor.execute(update_contact, (group_id, contato))
            connection.commit()
    except ProgrammingError as e:
        print(f'Error: {e.msg}')
    else:
        print(f'Updated {cursor.rowcount} registry')
