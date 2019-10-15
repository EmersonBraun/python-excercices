# Escreva um programa para aprovar o empréstimo bancário para a compra de uma casa.
# Pergunte o valor da casa, o salário do comprador e em quantos anos ele vai pagar.
# A prestação mensal não pode exceder 30% do salário ou então o empréstimo será negado

casa = float(input('Digite o valor da casa: '))
salario = float(input('Qual o salário bruto: '))
anos = int(input('Quantos anos pretende pagar: '))

parcela = casa / (anos * 12)
limite = salario * 0.3

print('Prestação R${:.2f} em {} anos'.format(parcela, anos))
print('Seu limite é R${:.2f}'.format(limite))
if parcela > limite:
    print('Empréstimo NEGADO!')
else:
    print('Empréstimo APROVADO! ')