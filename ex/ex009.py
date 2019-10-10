#tabuada
num = int(input('Digite um número: '))
print('=' * 20)
for i in range(1, 11):
    print('{} x {:2} = {}'.format(num, i, (num * i)))
print('=' * 20)