# Refaça o DESAFIO 035 dos triângulos, acrescentando o recurso de mostrar que tipo de triângulo será formado:
# - EQUILÁTERO: todos os lados iguais
# - ISÓSCELES: dois lados iguais, um diferente
# - ESCALENO: todos os lados diferentes

a = float(input('Digite uma reta: '))
b = float(input('Digite a segunda reta: '))
c = float(input('Digite a terceira reta: '))

if a < b + c and b < a + c and c < a + b:
    print('Com essas medidas \033[0;34mÉ\033[m possível fazer um triângulo ',end='')
    if a == b == c:
        print('EQUILÁTERO')
    elif a != b != c != a:
        print('ESCALENO')
    else:
        print('ISÓCELES')
else:
    print('Com essas medidas \033[0;31mNÃO É\033[m possível fazer um triângulo')