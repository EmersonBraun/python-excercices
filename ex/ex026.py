# Faça um programa que leia uma frase pelo teclado
# e mostre quantas vezes aparece a letra "?", em que posição ela aparece a primeira vez
# e em que posição ela aparece a última vez
string = str(input('Digite uma frase: ')).lower().strip()
letra = str(input('Digite uma letra: ')).lower()
print('A letra {} aparece {} vezes'.format(letra, string.count(letra)))
print('Primeira ocorrência: {}'.format(string.find(letra)+1))
print('Última ocorrência: {}'.format(string.rfind(letra)+1))
