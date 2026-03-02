# car rental
days = int(input('How many days did you keep the car: '))
kms = float(input('How many km driven: '))
price_per_day = float(input('Price per day: '))
price_per_km = float(input('Price per km: '))
total_day = days * price_per_day
total_km = kms * price_per_km
print('{:.2f} days + {:.2f} km, totaling R$: {:.2f}'.format(total_day, total_km, (total_day + total_km)))
