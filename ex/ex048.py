# Faça um programa que calcule a soma entre todos os números que são múltiplos de três 
# e que se encontram no intervalo de 1 até 500

print('Mútiplos de 3 entre 1 e 500\n')
total = 0
soma = 0
for c in range(1, 501, 2):
    if c % 3 == 0:
        soma += c
        total += 1
print('{} números e a soma é {}'.format(total, soma))
