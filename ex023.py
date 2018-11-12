#separar dígitos de um número
num = int(input('Informe um número: '))
print('Unidade: {} \nDezena: {}\nCentena: {}\nmilhar: {}\n'
      ''.format((num // 1 % 10) ,(num // 10 % 10), (num // 100 % 10),(num // 1000 % 10) ))