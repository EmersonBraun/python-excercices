# Faça um programa que leia três números
# e mostre qual é o maior e qual é o menor
num1 = float(input('Digite o primeiro número: '))
num2 = float(input('Digite o segundo número: '))
num3 = float(input('Digite o terceiro número: '))

numeros = [num1, num2, num3]
numeros = sorted(numeros)

print('O maior número é {} e o menor {}'.format(numeros[2], numeros[0]))