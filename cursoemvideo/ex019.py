# draw a random item from an array
from random import choice
n1 = input('First item: ')
n2 = input('Second item: ')
n3 = input('Third item: ')
n4 = input('Fourth item: ')
items = [n1, n2, n3, n4]
print('The chosen one was: {}'.format(choice(items)))
