# Write a program that reads the speed of a car.
# If it exceeds 80 km/h, show a message saying it was fined.
# The fine will cost R$7.00 per km above the limit
speed = float(input('Enter the speed: '))
if speed <= 80:
    print('Within the speed limit. ')
else:
    excess = speed - 80
    print('Above the speed limit!\nFine of R${:.2f}'.format(excess * 7))
