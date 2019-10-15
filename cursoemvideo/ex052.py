# Faça um programa que leia um número inteiro 
# e diga se ele é ou não um número primo

num = int(input('Digite um número para ver ser é primo: '))
cont = 0
print('{} é divisível por: '.format(num),end='')
for c in range(1, num + 1):
    if num % c == 0:
        print('{} ,'.format(c) ,end='')
        cont+=1
if cont <= 2:
    print('\nentão É um número primo!')
else:
    print('\nentão NÃO é um número primo!')