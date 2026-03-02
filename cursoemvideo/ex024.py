# Create a program that reads the name of a city
# and tells whether or not it starts with "?"
city = str(input('Enter the name of a city: ')).strip()
expected_start = str(input('Expected start: ')).strip()
print(city[:len(expected_start)].lower() == expected_start.lower())
