# Faça um programa que jogue par ou ímpar com o computador. 
# O jogo só será interrompido quando o jogador perder, 
# mostrando o total de vitórias consecutivas que ele conquistou no final do jogo

from random import randint
vitorias = 0
while True:
    jjogador = int(input('Digite um valor inteiro: '))
    pi_jogador = ' '
    while pi_jogador not in 'PpIi':
        pi_jogador = str(input('Par ou Impar? [P/I]')).strip().upper()[0]
    jpc = randint(0, 10) 

    total = jjogador + jpc
    resultado = "P" if total % 2 == 0 else "I" 
    print(f'Sua jogada foi {jjogador} e do computador {jpc}')
    print(f'O total foi {total} e é {resultado}')
    if resultado == pi_jogador:
        print('Você venceu!')
        vitorias += 1
    else:
        print('Você perdeu!')
        break
print(f'FIM DE JOGO! Foram {vitorias} vitorias')



