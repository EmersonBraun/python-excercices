# Elabore um programa que calcule o valor a ser pago por um produto,
# considerando o seu preço normal e condição de pagamento:
# - à vista dinheiro/cheque: 10% de desconto
# - à vista no cartão: 5% de desconto
# - em até 2x no cartão: preço formal
# - 3x ou mais no cartão: 20% de juros

print('{:=^40}'.format(' LOJA '))
compra = float(input('Preço da compra: R$'))
print('Formas de pagamento'
      '\n[ 1 ] à vista dinheiro/cheque'
      '\n[ 2 ] à vista no cartão:'
      '\n[ 3 ] em até 2x no cartão:'
      '\n[ 4 ] 3x ou mais no cartão:')
forma = int(input('Qual forma deseja pagar? '))

if forma == 1:
    modo = '10% de desconto)'
    total = compra * 0.9
elif forma == 2:
    modo = '5% de desconto'
    total = compra * 0.95
elif forma == 3:
    modo = 'preçço formal'
    total = compra
    print('Serão 2x de R${}'.format(compra / 2))
elif forma == 4:
    parcelas = int(input('Quantas parcelas? '))
    total = compra * 1.2
    modo = '20% de juros'
    print('Serão {} parcelas de {:.2f}'.format(parcelas, total / parcelas))
else:
    total = 0
    modo = ''
    print('Opção inválida!')
print('Sua compra fica de R${:.2f} por R${:.2f} ({})'.format(compra, total, modo))
