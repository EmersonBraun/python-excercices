#!/usr/bin/python3
def fibonacci():
    penultimo = 0
    ultimo = 1
    print(f'{penultimo},{ultimo}', end=',')
    while True:
        proximo = penultimo + ultimo
        print(proximo, end=',')
        penultimo = ultimo
        ultimo = proximo
        if(ultimo > 100):
            print('Fim')
            break


if __name__ == '__main__':
    fibonacci()
