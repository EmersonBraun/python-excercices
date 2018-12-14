#  Melhore o jogo do DESAFIO 028 onde o computador vai "pensar" em um número entre 0 e 10. 
# Só que agora o jogador vai tentar adivinhar até acertar, 
# mostrando no final quantos palpites foram necessários para vencer

from random import randint
randomico = randint(0, 10)
palpites = 0
print('=-'*20)
print('Vou pensar em um número entre 0 e 10.\n Tente adivinhar! ')
print('=-'*20)
while True:
    numero = int(input('Que número eu pensei? '))
    palpites += 1
    if numero == randomico:
        break
    if numero < randomico:
        print('\nMaior!')
    if numero > randomico :
        print('\nMenor!')
print('Acertou com {} palpites!'.format(palpites))

