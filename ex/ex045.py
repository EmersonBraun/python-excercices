# Crie um programa que faça o computador jogar Jokenpô com você

import emoji
import os
from random import randint
from time import sleep

opcoes = ('Pedra', 'Papel', 'Tesoura')
while True:
    print('=-'*20)
    print('{:^40}'.format(' JOGO JOKENPÔ '))
    print('=-'*20)
    
    computador = randint(0, 2)
    jogada = int(input('Suas opções:\n[ 0 ] PEDRA\n[ 1 ] PAPEL\n[ 2 ] TESOURA\nQual é a sua jogada? '))
    print('\nJO',end='')
    sleep(0.5)
    print('KEN',end='')
    sleep(0.5)
    print('PÔ\n')
    sleep(0.5)

    print('A sua jogada foi: {}'.format(opcoes[jogada]))
    print('A jogada do computador foi: {}'.format(opcoes[computador]))
    if computador == 0:
        if jogada == 0:
            print(emoji.emojize('EMPATE :ok_hand:', use_aliases=True))
        elif jogada == 1:
            print(emoji.emojize('VOCÊ GANHOU!!! :smile:', use_aliases=True))
        elif jogada == 2:
            print(emoji.emojize('VOCÊ PERDEU :sob:', use_aliases=True))
        else:
            print('Jogada inválida')

    elif computador == 1:
        if jogada == 0:
            print(emoji.emojize('VOCÊ PERDEU :sob:', use_aliases=True))
        elif jogada == 1:
            print(emoji.emojize('EMPATE :ok_hand:', use_aliases=True))
        elif jogada == 2:
            print(emoji.emojize('VOCÊ GANHOU!!! :smile:', use_aliases=True))
        else:
            print('Jogada inválida')

    elif computador == 2:
        if jogada == 0:
            print(emoji.emojize('VOCÊ GANHOU!!! :smile:', use_aliases=True))
        elif jogada == 1:
            print(emoji.emojize('VOCÊ PERDEU :sob:', use_aliases=True))
        elif jogada == 2:
            print(emoji.emojize('EMPATE :ok_hand:', use_aliases=True))
        else:
            print('Jogada inválida')
    print('\n')

    sair = str(input('Outra rodada? [s/n] ')).capitalize()
    if sair == 'N':
        sleep(0.2)
        print('\nSaindo', end='')
        sleep(0.5)
        print('.', end='')
        sleep(0.5)
        print('.', end='')
        sleep(0.5)
        print('.', end='')
        break
        SystemExit
    else:
        os.system('cls')


