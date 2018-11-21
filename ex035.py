# Desenvolva um programa que leia o comprimento de três retas
# e diga ao usuário se elas podem ou não formar um triângulo
a = float(input('Digite uma reta: '))
b = float(input('Digite a segunda reta: '))
c = float(input('Digite a terceira reta: '))

if a < b + c and b < a + c and c < a + b:
    print('Com essas medidas \033[0;34mÉ\033[m possível fazer um triângulo')
else:
    print('Com essas medidas \033[0;31mNÃO É\033[m possível fazer um triângulo')