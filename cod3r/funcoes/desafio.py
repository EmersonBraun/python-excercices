#!/usr/bin/python3
def tag(tag, *args, **kwargs):
    if 'html_class' in kwargs:
        kwargs['class'] = kwargs.pop('html_class')
    attrs = ' '.join(f'{key}="{value}"' for key, value in kwargs.items())
    inner = ''.join(args)
    return ''.join(f'<{tag} {attrs}>{inner}<{tag}/>')


if __name__ == '__main__':
    print(
        tag('p',
            tag('span', 'Curso de Python 3, aluno:'),
            tag('strong', 'Emerson Braun', id='eb'),
            tag('span', 'asd'),
            html_class='alert')
    )
