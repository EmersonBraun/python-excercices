# Crie um programa que mostre na tela todos os números pares 
# que estão no intervalo entre 1 e 50

print('Números pares entre 1 e 50:\n')
for c in range(1, 51):
    if c % 2 == 0:
        print(' {:2} '.format(c),end='')
        if(c % 10 == 0):
            print('\n')