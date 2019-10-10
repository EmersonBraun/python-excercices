#sortear um item de um array
from random import choice
n1 = input('Primeiro item: ')
n2 = input('Segundo item: ')
n3 = input('Terceiro item: ')
n4 = input('Quarto item: ')
list = [n1, n2, n3, n4]
print('O escolhido foi: {}'.format(choice(list)))