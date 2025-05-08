'''
модуль реалізує формування нормального закону
розподілу випадкової величини

модуль реалізує формування нормального закону
розподілу випадкової величини, як адитивна суміш двох рівномірних законів за
принципами циклічних повторень. Шляхом створення генераторної функції - RNgenerator
'''
from typing import Generator
import numpy as np
from math import sqrt, cos, log

def BBgenerator(n: int) -> Generator[float]:

    for _ in range(n):
        yield np.random.uniform()

def RNgenerator(n: int, v1:Generator[float], v2:Generator[float]) -> Generator[float]:

    c = 2 * np.pi
    for _ in range(n):
        yield sqrt(-2 * log(next(v1))) * cos( c * next(v2))

