# Refaça o DESAFIO 009, mostrando a tabuada de um número que o usuário escolher, 
# só que agora utilizando um laço for

num = int(input('Digite um número para ver sua tabuada:\ndigite 0 para tabuada completa '))
if num != 0:
    print('=' * 15)
    for i in range(1, 11):
        print('{} x {:2} = {}'.format(num, i, (num * i)))
    print('=' * 15)
else:
    for i in range(1, 11):
        print('=' * 15)
        for j in range(1, 11):
            print('{} x {:2} = {}'.format(i, j, (i * j)))
    print('=' * 15)


