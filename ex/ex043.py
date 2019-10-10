#  Desenvolva uma lógica que leia o peso e a altura de uma pessoa,
# calcule seu Índice de Massa Corporal (IMC) e mostre seu status,
# de acordo com a tabela abaixo:
# - IMC abaixo de 18,5: Abaixo do Peso
# - Entre 18,5 e 25: Peso Ideal
# - 25 até 30: Sobrepeso
# - 30 até 40: Obesidade
# - Acima de 40: Obesidade Mórbida

peso = float(input('Digite o peso em quilos: '))
altura = float(input('Digite a altura em metros: '))
imc = peso / (altura ** 2)

print('Seu imc é {:.2f} e você está '.format(imc),end='')
if imc < 18.5:
    print('abaixo do peso')
elif imc < 25:
    print('com peso ideal')
elif imc < 30:
    print('com sobrepeso')
elif imc < 40:
    print('com obesidade')
else:
    print('com obesidade mórbida')