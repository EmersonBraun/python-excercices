#!/usr/bin/python3
def fibonacci(quantidade):
    resultado = [0, 1]
    for _ in range(quantidade - 2):
        resultado.append(sum(resultado[-2:]))
    return resultado


if __name__ == '__main__':
    for fib in fibonacci(5):
        print(fib, end=',')
