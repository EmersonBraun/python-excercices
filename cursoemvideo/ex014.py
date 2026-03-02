# temperature converter
c = float(input('Enter the temperature in Celsius: '))
f = (c * 9/5) + 32
k = c + 273.15
print('The temperature {:.2f}°C equals {:.2f}°F and {:.2f}°K '.format(c, f, k))
