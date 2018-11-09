#conversor de moedas
real = float(input('Valor em R$: '))
dolar = float(3.7)
cotacao = real / dolar
print('R${:.2f} = US${:.2f}'.format(real, cotacao))