from math import pi


def circulo(raio):
    print('Área do circulo', pi * raio ** 2)


raio = float(input('Digite o raio:'))
circulo(raio)
