# Crie um programa que leia dois valores e mostre um menu na tela:
# [ 1 ] somar
# [ 2 ] multiplicar
# [ 3 ] maior
# [ 4 ] novos números
# [ 5 ] sair do programa
# Seu programa deverá realizar a operação solicitada em cada caso

n1 = int(input('Primeiro valor: '))
n2 = int(input('Segundo valor: '))
while True:
    print('O que deseja fazer? ')
    opt = int(input('[ 1 ] somar\n[ 2 ] multiplicar\n[ 3 ] maior\n[ 4 ] novos números\n[ 5 ] sair do programa\n'))
    if opt != 5:
        if opt == 1:
            print('\n{} + {} = {}'.format(n1, n2, n1+n2))
        elif opt == 2:
            print('\n{} * {} = {}'.format(n1, n2, n1*n2))
        elif opt == 3:
            if n1 > n2:
                print('\n{} é o maior'.format(n1))
            else:
                print('\n{} é o maior'.format(n2))
        elif opt == 4:
            n1 = int(input('Primeiro valor: '))
            n2 = int(input('Segundo valor: '))
        else:
            print('\nOpção inválida! ')
    else:
        break
   