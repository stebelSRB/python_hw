'''
У модулі описана функція FibExpression яка повертає генераторний об`єкт
'''
from typing import Generator

def FibExpression(n: int) -> Generator[int]:
    '''
    розраховує числа ряду Фібоначчі
    :param n номер послідовності
    '''
    return ( a := round(num / 1.9) if num < 3 else round(a * 1.618) for num in range(n + 1))
