#!/usr/bin/python3
from math import pi
import sys
import errno


class TerminalColor:
    ERRO = '\033[91m'
    NORMAL = '\033[0m'


def circulo(raio):
    return pi * float(raio) ** 2


def help(tipo):
    if(tipo == 'args'):
        print(TerminalColor.ERRO +
              "Necessário informar o raio do círculo" +
              TerminalColor.NORMAL)
    else:
        print(TerminalColor.ERRO +
              "Argumento deve ser numérico" +
              TerminalColor.NORMAL)
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
