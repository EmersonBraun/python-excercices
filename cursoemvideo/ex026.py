# Write a program that reads a phrase via keyboard
# and shows how many times the letter "?" appears, at what position it appears the first time
# and at what position it appears the last time
string = str(input('Enter a phrase: ')).lower().strip()
letter = str(input('Enter a letter: ')).lower()
print('The letter {} appears {} times'.format(letter, string.count(letter)))
print('First occurrence: {}'.format(string.find(letter) + 1))
print('Last occurrence: {}'.format(string.rfind(letter) + 1))
