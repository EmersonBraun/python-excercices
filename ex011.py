#pintar uma parede
largura = float(input('Insira a largura da parede: '))
altura = float(input('Insira a altura da parede: '))
area = largura * altura
latas = area/2
print('A parede de {}x{} tem área {:.2f}m² e serão necessárias {:.2f} latas'.format(largura, altura, area, latas))