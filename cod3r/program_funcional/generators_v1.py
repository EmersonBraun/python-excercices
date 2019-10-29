#!/usr/bin/python3
def cores_arcoiris():
    yield 'vermelho'
    yield 'laranja'
    yield 'amarelo'
    yield 'verde'
    yield 'azul'
    yield 'índigo'
    yield 'violeta'


if __name__ == '__main__':
    gerator = cores_arcoiris()
    while True:
        print(next(gerator))
