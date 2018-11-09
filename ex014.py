#conversor de temperaturas
c = float(input('Digite a temperatura em célsius: '))
f = (c * 9/5) + 32
k = c + 273.15
print('A temperatura {:.2f}°C equivale a {:.2f}°F e {:.2f}°K '.format(c, f, k))