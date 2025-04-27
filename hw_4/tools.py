
'''
Тут описані функції котрі модифікують зображення
'''

import numpy as np
from PIL import Image


# --------------------- інструменти для роботи з зображенням ----------------------
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