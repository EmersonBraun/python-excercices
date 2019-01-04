# Faça um programa que mostre a tabuada de vários números,
#  um de cada vez, para cada valor digitado pelo usuário. 
# O programa será interrompido quando o número solicitado for negativo

while True:
    tabuada = int(input('Quer ver qual tabuada? \n(negativo para sair) '))
    if tabuada < 0:
        break
    for c in range(1,11):
        print(f"{tabuada} x {c} = {tabuada * c}")
    print('=' * 20)
print('Sair')