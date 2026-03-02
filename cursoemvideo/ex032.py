# Write a program that reads any year
# and shows whether it is a leap year

from datetime import date
year = int(input('Which year do you want to analyze? (0 for current year) '))
if year == 0:
    year = date.today().year
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print('The year {} IS a leap year'.format(year))
else:
    print('The year {} IS NOT a leap year'.format(year))
