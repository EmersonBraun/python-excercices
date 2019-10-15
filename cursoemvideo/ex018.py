#seno, coseno e tangente
from math import radians, sin, cos, tan
ang = float(input('Digite um ângulo: '))
rad = radians(ang)
print('O ângulo de {} tem o SENO de {:.2f}, COSENO {:.2f} e TANGENTE {:.2f}'.format(ang, sin(rad), cos(rad), tan(rad)))