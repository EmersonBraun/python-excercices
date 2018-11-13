#primeiro e último nome
nome = str(input('Digite seu nome comleto: ')).strip().split()
print('Primeiro nome: {}\nÚltimo nome: {}'.format(nome[0], nome[len(nome)-1]))