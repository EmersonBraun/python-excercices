#!/usr/bin/python3
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def __str__(self):
        if not self.idade:
            return self.nome
        return f'{self.nome}: {self.idade} anos'

    def isAdult(self):
        return True if (self.idade >= 18 or 0) else False
