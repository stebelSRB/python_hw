
# --------------------------- Homework_6.2  ------------------------------------

'''

Виконав: Роман Стебельський

Homework_6.2 Принцип підстановки Барбари Лісков

'''


# Liskov
from abc import ABC, abstractmethod

class Vehicle(ABC):

    def __init__(self, driver: str):
        self.driver = driver

    @abstractmethod
    def go_vehicle(self) -> None:
        pass


class Car(Vehicle):

    def __init__(self, driver: str):
        super().__init__(driver)
        print(f"водій {driver} сів у машину")

    def start_engine(self) -> None:
        print("завів мотор")

    """A demo Car Vehicle class"""
    def go_vehicle(self) -> None:
        self.start_engine()
        print("і поїхав")


class Bicycle(Vehicle):

    def __init__(self, driver: str):
        super().__init__(driver)
        print(f"водій {driver} сів на велосипед")

    """A demo Bicycle Vehicle class"""
    def go_vehicle(self) -> None:
        print("і вже їде")

if __name__ == "__main__":

    v_car = Car('Володимир')
    v_car.go_vehicle()
    print('----------------------------------')
    s_bicycle = Bicycle('Сергій')
    s_bicycle.go_vehicle()

'''

Резюме:
    Метод start_engine актуальний тільки для моторних засобів,
    тому він відсутній у базовому класі Vehicle
    
    Метод go_vehicle актуальний для усіх транспортних засобів, тому:
        - результатом його роботи завжди є рух т.з.
        - реалізація початку руху може бути різною, тому у базовому класі описаний як абстрактний метод. 

Результат:

водій Володимир сів у машину
завів мотор
і поїхав
----------------------------------
водій Сергій сів на велосипед
і вже їде


'''