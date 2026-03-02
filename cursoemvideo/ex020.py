# The same teacher from challenge 019 wants to draw the presentation order of student assignments.
# Write a program that reads the names of four students and shows the drawn order
from random import shuffle
n1 = str(input('First item: '))
n2 = str(input('Second item: '))
n3 = str(input('Third item: '))
n4 = str(input('Fourth item: '))
items = [n1, n2, n3, n4]
shuffle(items)
print('The new order is: ')
print(items)
