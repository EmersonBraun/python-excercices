# Write a program that asks the salary of an employee and calculates their raise.
# For salaries above R$1250.00, calculate a 10% raise.
# For those below or equal, the raise is 15%

salary = float(input('Enter the employee salary: '))
if salary >= 1250:
    salary += salary * 0.1
else:
    salary += salary * 0.15
print('The salary will become R${:.2f}'.format(salary))
