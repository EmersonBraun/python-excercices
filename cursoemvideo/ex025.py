# Crie um programa que leia o nome de uma pessoa e diga se ela tem "?" no nome
string = str(input('Digite uma string: ')).strip()
coresp = str(input('valor esperado: ')).strip()
print(coresp.lower() in string.lower())