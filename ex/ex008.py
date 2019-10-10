#conversor de medidas
medida = float(input('Qual é a medida em metros: '))
cm = medida * 100
mm = medida * 1000
print('A medida em centímetros é {:.2f} e em milímetros {:.2f}'.format(cm, mm))