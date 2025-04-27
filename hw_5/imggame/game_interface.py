
'''
Модуль містить функцію яка надає інтерфейс користувачу для роботи з зображенням.

Цей модуль отримує функції (інструментів) для обробки зображень з методу та надає інтерфейс
користувачу який забезпечує використання цих інструментів та збереження модифікованого зображення.

Приклад застосування:
    from imggame import game_interface

    file_name_raw = "start.jpg"
    file_name_result = "stop.jpg"
    game_interface(file_name_raw, file_name_result)
'''

from .tools import Image, np
from . import tools
from matplotlib import pyplot as plt


#------------------------- опис функцій ---------------------------------
def game_interface(file_name_raw: str, file_name_result: str) -> None:

    '''
    Інтерфейс для завантаження/модифікації/збереження файлу з зображенням

    Функція завантажує файл з зображенням. Виводить інтерфейс в якому є можливість
    обрати команду(и):
        - модифікації зображення
        - збереження файлу з зображенням
        - відміна модифікації зображення шляхом повторного завантаження оригіналу
        - завершення обробки файлу без збереження

    :param file_name_raw: назва файлу з зображенням котре потрібно модифікувати.
    :param file_name_result: назва файлу в якому буде збережено модифіковане зображення.
    :return: не повертає жодного значення
    :exception FileNotFoundError: якщо файл не знайдено.
    :exception ValueError: якщо введено значення номера команди не є числом.
    '''

    command_set = '''
        1. завантажити оригінал
        2. повернути за годинниковою стрілкою
        3. повернути проти годинникової стрілки
        4. дзеркальне відображення по горизонталі
        5. дзеркальне відображення по вертикалі
        6. зменшити 
        7. зберегти
        8. завершити без збереження
    '''

    current_command = 0
    running = True
    print(command_set)

    try:
        img = Image.open(file_name_raw)
    except FileNotFoundError:
        running = False
        print(f'файлу з назвою {file_name_raw} не знайдено')

    while running:

        plt.imshow(img)
        plt.show()

        # запитуємо номер команди
        try:
            current_command = int(input('Вкажіть номер однієї з доступних команд:'))
        except ValueError:
            print('такої команди не існує, роботу завершено')
            running = False

        # шукаємо алгоритм обраної команди
        match current_command:
            case 1:
                img = Image.open(file_name_raw)
            case 7:
                print('зображення збережено')
                img.save(file_name_result, "JPEG")
                running = False
            case 8:
                print('роботу завершено без збереження зображення')
                running = False
            case 2 | 3 | 4 | 5 | 6:
                func_name = tools.tools_image[current_command]
                img_array = np.asarray(img)
                img = getattr(tools, func_name)(img_array)
            case _:
                print('такої команди не існує, роботу завершено')
                running = False

    return
