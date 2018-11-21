# Faça um programa que leia o nome completo de uma pessoa,
# mostrando em seguida o primeiro e o último nome separadamente
nome = str(input('Digite seu nome comleto: ')).strip().split()
print('Primeiro nome: {}\nÚltimo nome: {}'.format(nome[0], nome[len(nome)-1]))