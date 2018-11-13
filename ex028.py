#jogo da a divinhação
from random import randint
from time import sleep
randomico = randint(0, 5)
print('=-'*20)
print('Vou pensar em um número entre 0 e 5.\n Tente adivinhar! ')
print('=-'*20)
numero = int(input('Que número eu pensei? '))
print('Verificando')
#sleep(2)
if numero == randomico:
    print('\nACERTÔ MISERAVI!')
else:
    print('\nERRROUU, era {}'.format(randomico))
