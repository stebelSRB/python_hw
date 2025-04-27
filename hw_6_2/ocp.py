
# --------------------------- Homework_6.2  ------------------------------------

'''

Виконав: Роман Стебельський

Homework_6.2 Принцип відкритості/закритості

'''

# open/closed
from abc import ABC, abstractmethod

class Discount_base(ABC):

    def __init__(self, customer: str, price: float):
        self.customer = customer
        self.price = price

    @abstractmethod
    def give_discount(self) -> float:
        pass

class Discount_silver(Discount_base):

    def __init__(self, price: float):
        super().__init__('silver', price)

    def give_discount(self) -> float:
        return self.price * 0.2

class Discount_gold(Discount_base):

    def __init__(self, price: float):
        super().__init__('gold', price)

    def give_discount(self) -> float:
        return self.price * 0.3

class Discount_vip(Discount_base):

    def __init__(self, price: float):
        super().__init__('vip', price)

    def give_discount(self) -> float:
        return self.price * 0.4

if __name__ == "__main__":

    print(Discount_silver(100).give_discount())
    print(Discount_gold(100).give_discount())
    print(Discount_vip(100).give_discount())

'''

Результат:

    20.0
    30.0
    40.0



'''