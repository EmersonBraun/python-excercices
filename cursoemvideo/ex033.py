# Write a program that reads three numbers
# and shows which is the largest and which is the smallest
num1 = float(input('Enter the first number: '))
num2 = float(input('Enter the second number: '))
num3 = float(input('Enter the third number: '))

numbers = [num1, num2, num3]
numbers = sorted(numbers)

print('The largest number is {} and the smallest {}'.format(numbers[2], numbers[0]))
