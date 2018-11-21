# Crie um programa que leia o nome de uma cidade
# diga se ela começa ou não com o nome "?"
cidade = str(input('Digite o nome de uma cidade: ')).strip()
coresp = str(input('Começo esperado: ')).strip()
print(cidade[:len(coresp)].lower() == coresp.lower())