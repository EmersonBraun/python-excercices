#exercício para ver desconto de um produto
preco = float(input('Qual o valor do produto: '))
desconto = int(input('Qual é o valor do desconto: '))
print('O produto de R${:.2f} com desconto de {}% fica R$ {:.2f}'.format(preco, desconto, preco - (preco * desconto / 100)))