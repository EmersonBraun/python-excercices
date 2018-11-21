# Desenvolva um programa que pergunte a distância de uma viagem em Km.
# Calcule o preço da passagem, cobrando R$0,50 por Km para viagens de até 200Km
# e R$0,45 parta viagens mais longas

distancia = float(input('Digite a distância da viagem: '))
if distancia <= 200:
    total = distancia * 0.5
else:
    total = distancia * 0.45
print('O valor da viagem é de R${:.2f}'.format(total))