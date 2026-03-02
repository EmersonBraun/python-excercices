# Write a program that reads a number from 0 to 9999
# and shows each of the digits separately on screen
num = int(input('Enter a number: '))
print('Units: {} \nTens: {}\nHundreds: {}\nThousands: {}\n'
      ''.format((num // 1 % 10), (num // 10 % 10), (num // 100 % 10), (num // 1000 % 10)))
