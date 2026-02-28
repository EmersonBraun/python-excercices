# Create a program that reads the name of a person and tells if they have "?" in the name
string = str(input('Enter a string: ')).strip()
expected_value = str(input('Expected value: ')).strip()
print(expected_value.lower() in string.lower())
