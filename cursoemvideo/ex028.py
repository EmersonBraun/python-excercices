# Write a program that makes the computer "think" of an integer between 0 and 5
# and asks the user to try to guess the number chosen by the computer.
# The program should write on screen whether the user won or lost
from random import randint
from time import sleep
random_num = randint(0, 5)
print('=-' * 20)
print('I will think of a number between 0 and 5.\n Try to guess! ')
print('=-' * 20)
number = int(input('What number am I thinking of? '))
print('Checking')
sleep(2)
if number == random_num:
    print('\nCORRECT!')
else:
    print('\nWRONG, it was {}'.format(random_num))
