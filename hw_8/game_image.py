
'''
Цей модуль містить абстрактний клас game_image_base
та його дочірній клас game_image для модифікації зображень

    Цільові методи класу game_image:
        __turn_left - повертає зображення проти годинникової стрілки
        __turn_right - повертає зображення за годинниковою стрілкою
        __mirror_vertical - віддзеркалює зображення по вертикалі
        __mirror_horizon - віддзеркалює зображення по горизонталі
        __reduce - вдвічі зменшує зображення
'''

from abc import ABC, abstractmethod
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

class game_image_base(ABC):

    '''
    Абстрактний клас описує ключові атрибути та методи.

    :attribute img: екземпляр клусу зображення
    :attribute img_array: екземпляр матриці пікселей зображення
    :method show_image: виводить поточне зображення на екран
    tools_image: статичний метод повертає назву метода за номером
    '''

    @property
    @abstractmethod
    def img(self) -> Image.Image:
        pass

    @property
    @abstractmethod
    def img_array(self) -> np.ndarray:
        pass

    @abstractmethod
    def show_image(self) -> None:
        pass

class game_image(game_image_base):

    '''
    Клас побудований на основі абстрактного класу game_image_base
    '''

    def __init__(self, file_name_raw: str):
        self.__open_image(file_name_raw)

    @property
    def img(self) -> Image.Image:

        '''
        повертає екземпляр клусу зображення
        '''

        return self.__img

    @property
    def img_array(self) -> np.ndarray:

        '''
        повертає екземпляр матриці пікселей зображення
        '''

        return self.__img_array

    def __open_image(self, file_name_raw: str) -> None:

        '''
        зчитує файл з зображенням

        зчитує файл з зображенням в змінну self.__img та зберігає
        матрицю пікселей в змінну self.__img_array

        :param file_name_raw: назва файлу з зображенням.
        :exception FileNotFoundError: якщо файл не знайдено.
        '''

        try:
            self.__img = Image.open(file_name_raw)
            self.__img_array = np.asarray(self.__img)
        except FileNotFoundError:
            print(f'файлу з назвою {file_name_raw} не знайдено')
            self.__del__()

    def show_image(self) -> None:

        '''
        виводить поточне зображення на екран
        '''

        plt.imshow(self.__img)
        plt.show()

    @staticmethod
    def transform_image(func):

        def wrapper(self):
            self.__img_array = np.asarray(self.__img)
            try:
                func(self)
                self.__img = Image.fromarray(self.__img_array)
            except AttributeError:
                print('метод не визначено')

        return wrapper

    @staticmethod
    def get_tool(num_method: int) -> str:
        '''
        Повертає назву метода за номером

        перелік доступних інструментів:
            - 2: '__turn_right',
            - 3: '__turn_left',
            - 4: '__mirror_horizon',
            - 5: '__mirror_vertical',
            - 6: '__reduce'

        :param num_method: номер методу (інструменту)
        :exception AttributeError: якщо номер методу не визначено.
        '''
        tools_image = {
            2: 'turn_right',
            3: 'turn_left',
            4: 'mirror_horizon',
            5: 'mirror_vertical',
            6: 'reduce'
        }
        try:
            return tools_image[num_method]
        except KeyError:
            return ''

    #------------------------- опис методів трансформації зображення ---------------------------------
    @transform_image
    def turn_left(self) -> None:

        '''
        повертає зображення проти годинникової стрілки
        '''

        self.__img_array = np.flip(self.__img_array, 1)
        self.__img_array = self.__img_array.transpose((1, 0, 2))

    @transform_image
    def turn_right(self) -> None:

        '''
        повертає зображення за годинниковою стрілкою
        '''

        self.__img_array = self.__img_array.transpose((1, 0, 2))
        self.__img_array = np.flip(self.__img_array, 1)

    @transform_image
    def mirror_vertical(self) -> None:

        '''
        віддзеркалює зображення по вертикалі
        '''

        self.__img_array = np.flip(self.__img_array, 0)

    @transform_image
    def mirror_horizon(self) -> None:

        '''
        віддзеркалює зображення по горизонталі
        '''

        self.__img_array = np.flip(self.__img_array, 1)

    @transform_image
    def reduce(self) -> None:

        '''
        вдвічі зменшує зображення

        вдвічі зменшує зображення за рахунок зменшення матриці пікселей.
        Залишає кожен другий елемент нульової та першох осі.
        '''

        self.__img_array = self.__img_array[::2, ::2]

    def __del__(self):
        print('дякуємо що скористались нашим додатком.')