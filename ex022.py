# Crie um programa que leia o nome completo de uma pessoa e mostre:
# – O nome com todas as letras maiúsculas e minúsculas;
# – Quantas letras ao todo (sem considerar espaços);
# – Quantas letras tem o primeiro nome.
nome = str(input('Digite seu nome completo: ')).strip()
print('Em maiúsculas: {}'.format(nome.upper()))
print('Em minúsculas: {}'.format(nome.lower()))
print('Quantidade de caracteres (sem espaços): {}'.format(len(nome) - nome.count(' ')))
print('O primeiro nome tem {} caracteres'.format(nome.find(' ')))