# Escreva um programa que leia um número N inteiro qualquer 
# e mostre na tela os N primeiros elementos de uma Sequência de Fibonacci

print('=-'*20)
print('{:^40}'.format('Sequência Fibonacci'))
print('=-'*20)
termos = int(input('Quantos termos deseja exibir? '))
t1 = 0
t2 = 1
print('{}'.format(t1), end=' → ')
while termos != 0:
    t3 = t1
    t1 = t2
    t2 = t1 + t3
    print('{}'.format(t1), end=' → ')
    termos -= 1
print('FIM')