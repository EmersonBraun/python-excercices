# unit converter
measurement = float(input('What is the measurement in meters: '))
cm = measurement * 100
mm = measurement * 1000
print('The measurement in centimeters is {:.2f} and in millimeters {:.2f}'.format(cm, mm))
