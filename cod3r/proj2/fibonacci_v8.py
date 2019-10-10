#!/usr/bin/python3
def fibonacci(penultimo, ultimo):
    if ultimo > 100:
        return
    penultimo, ultimo = ultimo, penultimo + ultimo
    print(ultimo, end=',')
    fibonacci(penultimo, ultimo)


if __name__ == '__main__':
    print(0, 1, end=',')
    fibonacci(0, 1)
