#!/usr/bin/python3
from math import pi
import sys
import errno


def circulo(raio):
    return pi * float(raio) ** 2


def help(tipo):
    if(tipo == 'args'):
        print("Necessário informar o raio do círculo")
    else:
        print("Argumento deve ser numérico")
    print(f"Sintaxe: {sys.argv[0][2:]} <raio>")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        help('args')
        sys.exit(errno.EPERM)
    elif not sys.argv[1].isnumeric():
        help('tipo')
        sys.exit(errno.EINVAL)
    else:
        raio = sys.argv[1]
        area = circulo(raio)
        print('Área do círculo', area)
