# Create a program that reads the full name of a person and shows:
# – The name in all uppercase and lowercase letters;
# – How many letters in total (not counting spaces);
# – How many letters the first name has.
name = str(input('Enter your full name: ')).strip()
print('Uppercase: {}'.format(name.upper()))
print('Lowercase: {}'.format(name.lower()))
print('Character count (without spaces): {}'.format(len(name) - name.count(' ')))
print('The first name has {} characters'.format(name.find(' ')))
