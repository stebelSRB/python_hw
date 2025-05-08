'''
У модулі описаний клас RNiterator який реалізує ітератор для обчислення нормального закону
розподілу випадкової величини
'''
from typing import Generator
import numpy as np
from math import sqrt, cos, log

class RNiterator:

    def __init__(self, n:int, v1:Generator[float], v2:Generator[float]):
        self.start = 0
        self.end = n
        self.v1 = v1
        self.v2 = v2

    def __iter__(self):
        return self

    def __next__(self):
        if self.start >= self.end:
            raise StopIteration
        self.start += 1
        c = 2 * np.pi
        return sqrt(-2 * log(next(self.v1))) * cos(c * next(self.v2))