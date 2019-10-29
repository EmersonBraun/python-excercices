#!/usr/bin/python3
def mapear(funcao, lista):
    for l in lista:
        yield funcao(l)


if __name__ == '__main__':
    print(list(mapear(lambda x: x ** 2, [2, 3, 4])))
