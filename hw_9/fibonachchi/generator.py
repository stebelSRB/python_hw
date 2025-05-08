'''
У модулі описана генеративна функція FibGenerator
'''
from typing import Generator

def FibGenerator(n: int) -> Generator[int]:
    '''
    розраховує числа ряду Фібоначчі
    :param n номер послідовності
    '''
    a = 0
    b = 1
    yield a
    for i in range(n):
        a, b = b, a + b
        yield a

