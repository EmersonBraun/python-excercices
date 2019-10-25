#!/usr/bin/python3
from func_primeira_classe import dobro, quadrado


def processar(titulo, lista, funcao):
    print(f'Processando: {titulo}')
    for i in lista:
        print(i, '=>', funcao(i))


if __name__ == '__main__':
    processar('Dobros 1-10:', range(1, 11), dobro)
    processar('Quadrado 1-10:', range(1, 1), quadrado)
