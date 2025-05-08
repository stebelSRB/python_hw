'''
У модулі описаний клас FibIterator який реалізує ітератор для обчислення чисел Фібоначчі
'''

class FibIterator:

    def __init__(self, n:int):
        self.start = 0
        self.end = n
        self.fib = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.start > self.end:
            raise StopIteration
        self.fib = round(self.start / 1.9) if self.start < 3 else round(self.fib * 1.618)
        self.start += 1
        return self.fib