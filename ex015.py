#aluguel de carros
dias = int(input('Quantos dias ficou com o carro: '))
kms = float(input('Quantos km rodados: '))
valor_dia = float(input('Valor por dia: '))
valor_km = float(input('Valor por km: '))
total_dia = dias * valor_dia
total_km = kms * valor_km
print('{:.2f} dia + {:.2f} km, deu um total de R$: {:.2f}'.format(total_dia, total_km, (total_dia + total_km)))