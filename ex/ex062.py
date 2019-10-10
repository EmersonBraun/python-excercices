# Melhore o DESAFIO 061, 
# perguntando para o usuário se ele quer mostrar mais alguns termos.
# O programa encerrará quando ele disser que quer mostrar 0 termos

print('{:=^40}'.format('CALCULADORA PA'))
termo = int(input('Primeiro termo: '))
razao = int(input('Razão: '))
cont = 1
total = 0
mais = 10
while mais != 0:
    total += mais
    while cont <= total:
        print('{}->'.format(termo), end='')
        termo += razao
        cont += 1
    print('Pausa')
    mais = int(input('Quer ver mais quantos termos?'))
print('Foram mostrados {} termos'.format(total))