# Crie um programa que leia uma frase qualquer 
# e diga se ela é um palíndromo, 
# desconsiderando os espaços

frase = str(input('Digite uma frase: ')).strip().upper()
palavras = frase.split()
agrupadas = ''.join(palavras)
inverso = agrupadas[::-1]
print('O inverso de {} é {}'.format(agrupadas, inverso))
if inverso == agrupadas:
    print('É um PALÍNDROMO!')
else:
    print('Não é um PALÍNDROMO!')