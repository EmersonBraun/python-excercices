#  Refaça o DESAFIO 051, lendo o primeiro termo e a razão de uma PA, mostrando os 10 primeiros termos da progressão usando a estrutura while

print('{:=^40}'.format('CALCULADORA PA'))
termo = int(input('Primeiro termo: '))
razao = int(input('Razão: '))
cont = 1
while cont <= 10:
    print('{}->'.format(termo), end='')
    termo += razao
    cont += 1
print('Fim PA')