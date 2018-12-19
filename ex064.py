# Crie um programa que leia vários números inteiros pelo teclado. 
# O programa só vai parar quando o usuário digitar o valor 999, que é a condição de parada. 
# No final, mostre quantos números foram digitados e qual foi a soma entre eles 
# (desconsiderando o flag)

entrada = 0
contador = 0
soma = 0
while entrada != 999:
    entrada = int(input('Digite um número: [999 para parar] '))
    if entrada != 999:
        contador += 1
        soma += entrada
print(f'foram inseridos {contador} numeros e a soma deu {soma}')
