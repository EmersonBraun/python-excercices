#!/usr/bin/python3
def log(function):
    def decorator(*args, **kwargs):
        print(f'Função: {function.__name__}')
        print(f'args: {args}')
        print(f'kwargs: {kwargs}')
        resultado = function(*args, **kwargs)
        print(f'Resultado: {resultado}')
        return resultado
    return decorator


# @log
def soma(x, y):
    return x + y


@log
def sub(x, y):
    return x - y


if __name__ == '__main__':
    print(soma(1, 2))
