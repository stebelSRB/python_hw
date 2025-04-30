
'''
Цей модуль містить клас game_image2

клас game_image2 розширює можливості класу game_image

    нові методи:
        save_img - зберігає зображення у файл
        game_interface - Інтерфейс для завантаження/модифікації/збереження файлу з зображенням
'''

from game_image import game_image, Image, np

class game_image2(game_image):

    '''
    Клас побудований на основі класу game_image
    '''

    __command_set = '''
        1. завантажити оригінал
        2. повернути за годинниковою стрілкою
        3. повернути проти годинникової стрілки
        4. дзеркальне відображення по горизонталі
        5. дзеркальне відображення по вертикалі
        6. зменшити 
        7. зберегти
        8. завершити без збереження
    '''

    def __init__(self, file_name_raw: str, file_name_result: str):
        super().__init__(file_name_raw)
        self.file_name_result = file_name_result
        self.__file_name_raw = file_name_raw

    def save_img(self) -> None:
        '''
            зберігає зображення у файл
        '''

        self.img.save(self.file_name_result, "JPEG")

    def game_interface(self) -> None:

        '''
        Інтерфейс для завантаження/модифікації/збереження файлу з зображенням

        :exception ValueError: якщо введено значення номера команди не є числом.
        '''

        current_command = 0
        running = True
        print(self.__command_set)

        while running:

            self.show_image()

            # запитуємо номер команди
            try:
                current_command = int(input('Вкажіть номер однієї з доступних команд:'))
            except ValueError:
                print('такої команди не існує, роботу завершено')
                running = False

            # шукаємо алгоритм обраної команди
            match current_command:
                case 1:
                    self.__open_image(self.__file_name_raw)
                case 7:
                    print('зображення збережено')
                    self.save_img()
                    running = False
                case 8:
                    print('роботу завершено без збереження зображення')
                    running = False
                case 2 | 3 | 4 | 5 | 6:
                    name_method = game_image.get_tool(current_command)
                    getattr(self, name_method)()
                case _:
                    print('такої команди не існує, роботу завершено')
                    running = False

    def __del__(self):
        print('ви працювали з файлом - ' + self.__file_name_raw)