#verificar igualdade strings
cidade = str(input('Digite o nome de uma cidade: ')).strip()
coresp = str(input('Começo esperado: ')).strip()
print(cidade[:len(coresp)].lower() == coresp.lower())