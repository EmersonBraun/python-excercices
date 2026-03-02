# exercise to calculate product discount
price = float(input('What is the product price: '))
discount = int(input('What is the discount value: '))
print('The product of R${:.2f} with {}% discount becomes R$ {:.2f}'.format(price, discount, price - (price * discount / 100)))
