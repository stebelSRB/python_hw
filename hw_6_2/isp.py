
# --------------------------- Homework_6.2  ------------------------------------

'''

Виконав: Роман Стебельський

Homework_6.2 Принцип розділення інтерфейсів

'''

# Interface segregation
from abc import ABC, abstractmethod

class Worker(ABC):

    @abstractmethod
    def get_a_salary(self) -> None:
        pass

class Builder(Worker):

    def build_construction(self) -> None:
        print("No! I have a dinner!")

    def get_a_salary(self) -> None:
        print("it's ok!")

class Waiter(Worker):
    
    def serve_the_table(self) -> None:
        print("Going to table")

    def get_a_salary(self) -> None:
        print("good tips!")
    
class Teacher(Worker):

    def check_hometask(self) -> None:
        print("Students are so talented!")

    def get_a_salary(self) -> None:
        print("and a prize!")
        


'''


'''