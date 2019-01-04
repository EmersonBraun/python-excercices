# Crie um programa que leia números inteiros pelo teclado. 
# O programa só vai parar quando o usuário digitar o valor 999, 
# que é a condição de parada. No final, mostre quantos números foram digitados 
# e qual foi a soma entre elas (desconsiderando o flag)
cont = 0
total = 0

while True:
    num = int(input('Digite um número: [999 para sair] '))
    if num == 999:
        break
    else:
        cont += 1
        total += num
print(f"foram digitados {cont} números, com soma igual a {total}")