# breaking a number (with library)
from math import trunc
num = float(input('Enter a value: '))
print('The value entered was {} and its integer portion is {}'.format(num, trunc(num)))
