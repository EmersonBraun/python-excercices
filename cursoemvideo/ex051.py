# Desenvolva um programa que leia o primeiro termo e a razão de uma PA. 
# No final, mostre os 10 primeiros termos dessa progressão

print('{:=^40}'.format('CALCULADORA PA'))
primeiro = int(input('Primeiro termo: '))
razao = int(input('Razão: '))
quantidade = int(input('Quantidade a ser mostrada: '))
mostrada = primeiro + (quantidade - 1) * razao 
for c in range(primeiro, mostrada + razao, razao):
    print('{}'.format(c), end='->')
print('Fim PA')