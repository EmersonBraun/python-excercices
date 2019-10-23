#!/usr/bin/python3
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def isAdult(self):
        return True if self.idade >= 18 else False


class Vendedor(Pessoa):
    def __init__(self, nome, idade, salario):
        super().__init__(nome, idade)
        self.salario = salario


class Cliente(Pessoa):
    def __init__(self, nome, idade):
        super().__init__(nome, idade)
        self.compras = []

    def registrar_compra(self, compra):
        self.compras.append(compra)

    def get_data_ultima_compra(self):
        pass

    def total_compras(self):
        pass


class Compra:
    def __init__(self, vendedor, data, valor):
        self.vendedor = vendedor
        self.data = data
        self.valor = valor
