# sine, cosine and tangent
from math import radians, sin, cos, tan
angle = float(input('Enter an angle: '))
rad = radians(angle)
print('The angle of {} has SINE of {:.2f}, COSINE {:.2f} and TANGENT {:.2f}'.format(angle, sin(rad), cos(rad), tan(rad)))
