# painting a wall
width = float(input('Enter the wall width: '))
height = float(input('Enter the wall height: '))
area = width * height
cans = area / 2
print('The wall of {}x{} has area {:.2f}m² and will require {:.2f} cans'.format(width, height, area, cans))
