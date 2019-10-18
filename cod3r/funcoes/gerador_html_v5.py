#!/usr/bin/python3
bloco_atrs = ('bloco_accesskey', 'bloco_id')
ul_atrs = ('ul_id', 'ul_style')


def get_atrs(informados, suportados):
    return ' '.join(f'{key.split("_")[-1]}="{value}"'
                    for key, value in informados.items() if key in suportados)


def tag_bloco(conteudo, *args, classe='success', inline=False, **novos_atrs):
    tag = 'span' if inline else 'div'
    html = conteudo if not callable(
        conteudo) else conteudo(*args, **novos_atrs)
    atributos = get_atrs(novos_atrs, bloco_atrs)
    return f'<{tag} {atributos} class="{classe}">{html}</{tag}>'


def tag_lista(*itens, **novos_atrs):
    lista = ''.join((f'<li>{item}</li>' for item in itens))
    return f'<ul {get_atrs(novos_atrs, ul_atrs)}>{lista}</ul>'


if __name__ == '__main__':
    # print(tag_bloco('bloco'))
    # print(tag_bloco('Inline e classe', 'info', True))
    # print(tag_bloco('inline', inline=True))
    # print(tag_bloco('falhou', classe='error'))
    # print(tag_lista('ana', 'josé', 'maria'))
    # print(tag_bloco(tag_lista('Item 1', 'item 2', 'item 3'),
    #                 classe='success', inline=False))
    # print(tag_bloco(tag_lista, 'Sábado', 'Domingo',
    #                 classe='success', inline=True))
    print(tag_bloco(tag_lista, 'Item 1', 'Item 2', classe='success',
                    bloco_accesskey='m', bloco_id='conteudo', ul_id='lista'))
