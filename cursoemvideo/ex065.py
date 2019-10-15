# Crie um programa que leia vários números inteiros pelo teclado. 
# No final da execução, mostre a média entre todos os valores 
# e qual foi o maior e o menor valores lidos. 
# O programa deve perguntar ao usuário se ele quer ou não continuar a digitar valores
cont = 0
total = 0
continua = 'S'
while True:
    entrada = int(input('Digite um número inteiro: '))
    if cont == 0:
        maior = entrada
        menor = entrada
    else:
        if entrada > maior:
            maior = entrada
        if entrada < menor:
            menor = entrada
    total += entrada
    cont += 1
    continua = str(input('Deseja continuar? [S/N] ')).strip().upper()[0]
    if continua == 'N':
        break
    if continua == 'S':
        continue
    if continua not in 'SN':
        print('Opção inválida! ')
print(f"\nForam lidos {cont} números \ncom a média de: {total/cont}\no menor: {menor}\no maior: {maior} ")
    
