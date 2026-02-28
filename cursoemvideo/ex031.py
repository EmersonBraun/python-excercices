# Develop a program that asks the distance of a trip in km.
# Calculate the ticket price, charging R$0.50 per km for trips up to 200 km
# and R$0.45 for longer trips

distance = float(input('Enter the trip distance: '))
if distance <= 200:
    total = distance * 0.5
else:
    total = distance * 0.45
print('The trip cost is R${:.2f}'.format(total))
