# Desenvolva um programa que leia o nome, idade e sexo de 4 pessoas. 
# No final do programa, mostre: a média de idade do grupo, 
# qual é o nome do homem mais velho 
# e quantas mulheres têm menos de 20 anos

totalidade = 0
maisvelho = 0
nomevelho = ''
menosde20 = 0
for c in range(1, 5):
    print('-'*10)
    print('{} pessoa'.format(c))
    nome = str(input('Nome: ')).strip()
    idade = int(input('Idade: '))
    sexo = str(input('Sexo [M/F]: ')).strip().upper()
    totalidade += idade
    if c == 1 and sexo == 'M':
        maisvelho = idade
        nomevelho = nome
    if idade > maisvelho and sexo == 'M':
        maisvelho = idade
        nomevelho = nome
    if idade < 20 and sexo == 'F':
        menosde20 += 1
print('\nA média de idade do grupo é {} anos'.format(totalidade / 4))
print('O homem mais velho tem {} anos e se chama {}'.format(maisvelho, nomevelho))
print('Há {} mulheres com menos de 20 anos'.format(menosde20))
