#!/usr/bin/python3
from locale import setlocale, LC_ALL
from calendar import mdays, month_name
from functools import reduce

setlocale(LC_ALL, 'pt_BR.UTF-8')


meses_maiores = filter(lambda indice: mdays[indice] == 31, range(1, 13))
nome_meses = map(lambda nome: month_name[nome], meses_maiores)
juntar_meses = reduce(lambda meses, nome_mes: f'{meses}\n- {nome_mes}',
                      nome_meses, 'Meses com 31 dias:')
print(juntar_meses)
