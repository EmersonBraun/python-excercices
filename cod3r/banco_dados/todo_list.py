import sys
from sqlite3 import connect, ProgrammingError, Row

tabela = """
    CREATE TABLE IF NOT EXISTS todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        descricao VARCHAR(30), 
        feito boolean)"""
pendentes = 'SELECT id, descricao FROM todo WHERE not feito'
adicionar = 'INSERT INTO todo (descricao, feito) VALUES (?, false)'
concluir = 'UPDATE todo SET feito = true WHERE id = ?'
try:
    conexao = connect('todo.db')
    conexao.row_factory = Row
    cursor = conexao.cursor()
    cursor.execute(tabela)

    while True:
        cursor.execute(pendentes)
        tarefas = cursor.fetchall()
        for i, tarefa in enumerate(tarefas, start=1):
            print(f'{i} - {tarefa["descricao"]}')
        print()
        print('Indique o número de uma tarefa para concluir, digite uma nova tarefa ou "sair":')
        entrada = input(':')

        if entrada.lower() == 'sair':
            sys.exit(0)

        if entrada.isnumeric() and int(entrada) in range(1, len(tarefas) + 1):
            cursor.execute(concluir, (tarefas[int(entrada)-1]['id'],))
        elif entrada.strip() and not entrada.isnumeric():
            cursor.execute(adicionar, (entrada.strip(),))
        else:
            print('> entrada inválida!')

        conexao.commit()
except ProgrammingError as e:
    print(f'Erro: {e.msg}')
