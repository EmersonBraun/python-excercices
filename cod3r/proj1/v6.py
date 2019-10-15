#!/usr/bin/python3
from math import pi


def circulo(raio):
    return pi * raio ** 2


raio = float(input('Digite o raio:'))
area = circulo(raio)
print('Área do círculo', area)
