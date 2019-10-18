#!/usr/bin/python3
def soma_n(*numeros):
    soma = 0
    for n in numeros:
        soma += n
    return soma


if __name__ == '__main__':
    # packing
    print(soma_n(1, 1, 1, 1, 1, 1, 1))
    # unpacking
    tupla_nums = (1, 2, 3)
    print(soma_n(*tupla_nums))
