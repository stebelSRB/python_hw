
'''
Цей модуль містить функції для модифікації зображень

    Функції:
        turn_left - повертає зображення проти годинникової стрілки
        turn_right - повертає зображення за годинниковою стрілкою
        mirror_vertical - віддзеркалює зображення по вертикалі
        mirror_horizon - віддзеркалює зображення по горизонталі
        reduce - вдвічі зменшує зображення

    tools_image - словник який містить всі назви функцій які описані у модулі.
    Кожна функція закріплена за конкретним номером.
'''

import numpy as np
from PIL import Image

# назви функцій для обробки зображення
tools_image = {
    2: 'turn_right',
    3: 'turn_left',
    4: 'mirror_horizon',
    5: 'mirror_vertical',
    6: 'reduce'
}

#------------------------- опис функцій ---------------------------------
def turn_left(img_array: np.ndarray) -> Image.Image:

    '''
    повертає зображення проти годинникової стрілки

    :param img_array: матриця пікселей у вигляді масиву 3-D.
    Третій рівень матриці має три елементи (RGB).
    :return: об'єкт зображення`~PIL.Image.Image`.
    '''

    img_array = np.flip(img_array, 1)
    img_array = img_array.transpose((1, 0, 2))

    return Image.fromarray(img_array)

def turn_right(img_array: np.ndarray) -> Image.Image:

    '''
    повертає зображення за годинниковою стрілкою

    :param img_array: матриця пікселей у вигляді масиву 3-D.
    Третій рівень матриці має три елементи (RGB).
    :return: об'єкт зображення`~PIL.Image.Image`.
    '''

    img_array = img_array.transpose((1, 0, 2))
    img_array = np.flip(img_array, 1)

    return Image.fromarray(img_array)

def mirror_vertical(img_array: np.ndarray) -> Image.Image:

    '''
    віддзеркалює зображення по вертикалі

    :param img_array: матриця пікселей у вигляді масиву 3-D.
    Третій рівень матриці має три елементи (RGB).
    :return: об'єкт зображення`~PIL.Image.Image`.
    '''

    img_array = np.flip(img_array, 0)

    return Image.fromarray(img_array)

def mirror_horizon(img_array: np.ndarray) -> Image.Image:

    '''
    віддзеркалює зображення по горизонталі

    :param img_array: матриця пікселей у вигляді масиву 3-D.
    Третій рівень матриці має три елементи (RGB).
    :return: об'єкт зображення`~PIL.Image.Image`.
    '''

    img_array = np.flip(img_array, 1)

    return Image.fromarray(img_array)

def reduce(img_array: np.ndarray) -> Image.Image:

    '''
    вдвічі зменшує зображення

    вдвічі зменшує зображення за рахунок зменшення матриці пікселей.
    Залишає кожен другий елемент нульової та першох осі.

    :param img_array: матриця пікселей у вигляді масиву 3-D.
    Третій рівень матриці має три елементи (RGB).
    :return: об'єкт зображення`~PIL.Image.Image`.
    '''

    img_array = img_array[::2, ::2]

    return Image.fromarray(img_array)
