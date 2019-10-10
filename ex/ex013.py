#calculando reajuste salarial
preco = float(input('Qual o valor do salário: '))
aumento = int(input('Qual é o percentual do aumento: '))
print('O salário de R${:.2f} com aumento de {}% fica R$ {:.2f}'.format(preco, aumento, preco + (preco * aumento / 100)))