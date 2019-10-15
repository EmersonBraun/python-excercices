# Crie um programa que leia o ano de nascimento de sete pessoas. 
# No final, mostre quantas pessoas ainda não atingiram a maioridade e quantas já são maiores

from datetime import date
atual = date.today().year
menor = 0
maior = 0
for c in range(1, 8):
    nascimento = int(input('Ano de nascimento da {}ª pessoa: '.format(c)))
    if atual - nascimento < 18:
        menor += 1
    else:
        maior += 1
print('\n{} menores e {} maiores'.format(menor, maior))