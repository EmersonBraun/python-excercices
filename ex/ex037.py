# Escreva um programa em Python que leia um número inteiro qualquer
# e peça para o usuário escolher qual será a base de conversão:
# 1 para binário, 2 para octal e 3 para hexadecimal

print('=-'*20)
print('Conversor de bases numéricas')
num = int(input('Digite um número inteiro: '))
print('[ 1 ] Binário\n[ 2 ] octal\n[ 3 ] hexadecimal ')
opcao = int(input('qual base quer transformar:'))
if opcao == 1:
    print('O número {} em binário fica {}'.format(num, bin(num)[2:]))
elif opcao == 2:
    print('O número {} em octal fica {}'.format(num, oct(num)[2:]))
elif opcao == 3:
    print('O número {} em hexadecimal fica {}'.format(num, hex(num)[2:]))
else:
    print('Opção incoreta!')