# O mesmo professor do desafio 019 quer sortear a ordem de apresentação de trabalhos dos alunos.
# Faça um programa que leia o nome dos quatro alunos e mostre a ordem sorteada
from random import shuffle
n1 = str(input('Primeiro item: '))
n2 = str(input('Segundo item: '))
n3 = str(input('Terceiro item: '))
n4 = str(input('Quarto item: '))
list = [n1, n2, n3, n4]
shuffle(list)
print('A nova ordem fica: ')
print(list)