# Faça um programa que leia o ano de nascimento de um jovem
# e informe, de acordo com a sua idade, se ele ainda vai se alistar ao serviço militar,
# se é a hora exata de se alistar ou se já passou do tempo do alistamento.
# Seu programa também deverá mostrar o tempo que falta ou que passou do prazo

from datetime import date
nascimento = int(input('Ano de nascimento: '))
anoAtual = date.today().year
idade = anoAtual - nascimento

print('Quem nasceu em {} tem {} anos em {}'.format(nascimento, idade, anoAtual))
if idade < 18:
    print('Ainda vai se alistar, faltam {} anos'.format(18 - idade))
    print('Seu alistamento será em {}'.format(nascimento + 18))
elif idade > 18:
    print('Já passaram {} anos do tempo de se alistar'.format(idade - 18))
    print('Seu alistamento foi em {}'.format(nascimento + 18))
else:
    print('Está na hora de se alistar!')