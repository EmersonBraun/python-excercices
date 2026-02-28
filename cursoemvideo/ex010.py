# currency converter
real = float(input('Value in R$: '))
dollar = float(3.7)
rate = real / dollar
print('R${:.2f} = US${:.2f}'.format(real, rate))
