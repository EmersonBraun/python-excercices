#!/usr/bin/python3
from datetime import datetime
from loja import Cliente, Vendedor, Compra


def main():
    cliente = Cliente('Dougras', 17)
    vendedor = Vendedor('Silas Car', 36, 1000)
    compra1 = Compra(cliente, datetime.now(), 512)
    compra2 = Compra(cliente, datetime.now(), 530)
    cliente.registrar_compra(compra1)
    cliente.registrar_compra(compra2)
    print(f'Cliente : {cliente.nome}')
    print(f'Vendedor : {vendedor.nome}')

    valor_total = cliente.total_compras()
    qtd_compras = len(cliente.compras)
    print(f'Total: {valor_total} em {qtd_compras} compras')
    print(f'Última compra: {cliente.get_data_ultima_compra()}')


main()
