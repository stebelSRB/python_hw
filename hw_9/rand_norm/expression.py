'''
модуль реалізує формування нормального закону
розподілу випадкової величини

модуль реалізує формування нормального закону
розподілу випадкової величини, як адитивна суміш двох рівномірних законів за
принципами циклічних повторень. Шляхом створення генераторного виразу - RNexpression
'''
from typing import Generator
import numpy as np
from math import sqrt, cos, log

def RNexpression(n: int) -> Generator[float]:
    v1 = (np.random.uniform() for _ in range(n))
    v2 = (np.random.uniform() for _ in range(n))
    c = 2 * np.pi
    return (sqrt(-2 * log(next(v1))) * cos( c * next(v2)) for _ in range(n))

