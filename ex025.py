#procurar string dentro de outra string
string = str(input('Digite uma string: ')).strip()
coresp = str(input('valor esperado: ')).strip()
print(coresp.lower() in string.lower())