#!/usr/bin/python3
class Carro:
    def __init__(self, velMax=180):
        self.velMax = velMax
        self.velAtual = 0
        self.velMin = 0

    def acelerar(self, kmh=5):
        maxima = self.velMax
        velEsperada = self.velAtual + kmh
        self.velAtual = velEsperada if velEsperada <= maxima \
            else maxima
        return self.velAtual

    def freiar(self, kmh=5):
        velEsperada = self.velAtual - kmh
        self.velAtual = velEsperada if velEsperada >= self.velMin \
            else self.velMin
        return self.velAtual


if __name__ == '__main__':
    c1 = Carro(200)

    for _ in range(25):
        print(_, c1.acelerar(8))

    for _ in range(10):
        print(_, c1.freiar(20))
