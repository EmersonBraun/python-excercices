# multiplication table
num = int(input('Enter a number: '))
print('=' * 20)
for i in range(1, 11):
    print('{} x {:2} = {}'.format(num, i, (num * i)))
print('=' * 20)
