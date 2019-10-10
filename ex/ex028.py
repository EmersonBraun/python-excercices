# Escreva um programa que faça o computador "pensar" em um número inteiro entre 0 e 5
# e peça para o usuário tentar descobrir qual foi o número escolhido pelo computador.
# O programa deverá escrever na tela se o usuário venceu ou perdeu
from random import randint
from time import sleep
randomico = randint(0, 5)
print('=-'*20)
print('Vou pensar em um número entre 0 e 5.\n Tente adivinhar! ')
print('=-'*20)
numero = int(input('Que número eu pensei? '))
print('Verificando')
sleep(2)
if numero == randomico:
    print('\nACERTÔ MISERAVI!')
else:
    print('\nERRROUU, era {}'.format(randomico))
