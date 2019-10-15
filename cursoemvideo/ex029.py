# Escreva um programa que leia a velocidade de um carro.
# Se ele ultrapassar 80Km/h, mostre uma mensagem dizendo que ele foi multado.
# A multa vai custar R$7,00 por cada Km acima do limite
velocidade = float(input('Digite a veloccidade: '))
if velocidade <= 80:
    print('Dentro do limite de velocidade. ')
else:
    excedente = velocidade - 80
    print('Acima do limite de velocidade!\nMulta de R${:.2f}'.format(excedente * 7))