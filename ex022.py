#manipulação de strings
nome = str(input('Digite seu nome completo: ')).strip()
print('Em maiúsculas: {}'.format(nome.upper()))
print('Em minúsculas: {}'.format(nome.lower()))
print('Quantidade de caracteres (sem espaços): {}'.format(len(nome) - nome.count(' ')))
print('O primeiro nome tem {} caracteres'.format(nome.find(' ')))