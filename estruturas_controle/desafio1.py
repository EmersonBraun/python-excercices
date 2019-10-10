#!/usr/bin/python3
import sys


class TerminalColor:
    ERRO = '\033[91m'
    NORMAL = '\033[0m'


def conceito(nota):
    valor = float(nota)
    if 10 > valor < 1:
        return "Nota inválida"
    elif valor >= 9.1:
        return "A"
    elif valor >= 8.1:
        return "A-"
    elif valor >= 7.1:
        return "B"
    elif valor >= 6.1:
        return "B-"
    elif valor >= 5.1:
        return "C"
    elif valor >= 4.1:
        return "C-"
    elif valor >= 3.1:
        return "D"
    elif valor >= 2.1:
        return "D-"
    elif valor >= 1.1:
        return "E"
    else:
        return "E-"


def verifica_tipo():
    if len(sys.argv) < 2:
        return [False, 'Nota não informada']
    elif not sys.argv[1].isnumeric():
        return [False, 'Tipo inválido, deve ser INT ou FLOAT']
    else:
        return [True, 'OK']


def help():
    testeTipo = verifica_tipo()
    if testeTipo[0] is False:
        print(TerminalColor.ERRO + testeTipo[1] + TerminalColor.NORMAL)
        print(f"Sintaxe: {sys.argv[0][2:]} <raio>")
        sys.exit(1)


if __name__ == '__main__':
    help()
    nota = sys.argv[1]
    conceito = conceito(nota)
    print(f'Conceito: {conceito}')
