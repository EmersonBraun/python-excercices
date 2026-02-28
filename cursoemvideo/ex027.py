# Write a program that reads the full name of a person,
# then shows the first and last name separately
name = str(input('Enter your full name: ')).strip().split()
print('First name: {}\nLast name: {}'.format(name[0], name[len(name) - 1]))
