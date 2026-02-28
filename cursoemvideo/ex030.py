# Create a program that reads an integer and shows on screen if it is EVEN or ODD
num = int(input('Enter a number: '))
if num % 2 == 0:
    kind = 'EVEN'
else:
    kind = 'ODD'
print('The number {} is {}'.format(num, kind))
