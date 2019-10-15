#!/usr/bin/python3
def fibonacci(quantiade, sequencia=(0, 1)):
    return sequencia if len(sequencia) == quantiade else \
        fibonacci(quantiade, sequencia + (sum(sequencia[-2:]),))


if __name__ == '__main__':
    for fib in fibonacci(20):
        print(fib)
