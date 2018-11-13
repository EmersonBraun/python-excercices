#leia a velocidade de um carro, se ultrapassar 80km, multa de R$7 por km excedente
velocidade = float(input('Digite a veloccidade: '))
if velocidade <= 80:
    print('Dentro do limite de velocidade. ')
else:
    excedente = velocidade - 80
    print('Acima do limite de velocidade!\nMulta de R${:.2f}'.format(excedente * 7))