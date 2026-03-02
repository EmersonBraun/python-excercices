# calculating salary adjustment
price = float(input('What is the salary value: '))
raise_pct = int(input('What is the raise percentage: '))
print('The salary of R${:.2f} with a {}% raise becomes R$ {:.2f}'.format(price, raise_pct, price + (price * raise_pct / 100)))
