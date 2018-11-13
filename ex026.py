#quantidade de ocorências de uma letra em uma string
string = str(input('Digite uma frase: ')).lower().strip()
letra = str(input('Digite uma letra: ')).lower()
print('A letra {} aparece {} vezes'.format(letra, string.count(letra)))
print('Primeira ocorrência: {}'.format(string.find(letra)+1))
print('Última ocorrência: {}'.format(string.rfind(letra)+1))
