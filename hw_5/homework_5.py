# --------------------------- Homework_5  ------------------------------------

'''

Виконав: Роман Стебельський
Homework_5, ІI рівень складності:

    Реалізовано:
        Два пакети на основі програм з ДЗ 3 та 4, парсер сайту - parssite та модифікація зображення - imggame.

        Пакет imggame:
            - Містить два модулі tools та game_interface.
            - На відміну від ДЗ4 оновлено документація модулів.
            - На відміну від ДЗ4 модуль tools отримав словник tools_image з переліком команд, який
            раніше був описаний у функції game_with_image модуль interface.
            - Модуль game_interface імпортує модуль tools і разом з ним бібліотеки pandas та pillow
            - Налаштуваня __init__, from imggame import game_interface імпортує безпосередньо функцію

        Пакет parssite:
            - містить чотири модулі api_nbu, parser_artmobile, http_request, load_price
            - модулі імпортують один одного
                load_price
                    <- parser_artmobile
                        <- http_request
                    <- api_nbu
                        <- http_request


Package            Version
------------------ -----------
pandas             2.2.3
pillow             11.2.1
pip                23.2.1
matplotlib         3.10.1
numpy              2.2.4
requests           2.32.3
bs4                0.0.2
lxml               5.3.2

'''

import imggame
from imggame import game_interface
from parssite import api_nbu, parser_artmobile, load_price

# ---------------------------------- головні виклики --------------------------------
if __name__ == "__main__":

    print('переглядаємо документацію пакету imggame')
    help(imggame)

    print('-------------------------------------')

    print('переглядаємо документацію модуля load_price')
    help(load_price)

    print('-------------------------------------')

    print('демонстрація роботи функції game_interface з пакету imggame модуль game_interface')
    file_name_raw = "start.jpg"
    file_name_result = "stop.jpg"
    game_interface(file_name_raw, file_name_result)

    print('-------------------------------------')

    print('демонстрація роботи функції get_exchange_rate з пакету parssite модуль api_nbu')
    exchange_rate = api_nbu.get_exchange_rate(['USD'])
    print(exchange_rate)

    print('-------------------------------------')

    print('демонстрація роботи функції pars_categories з пакету parssite модуль parser_artmobile')
    url = 'https://artmobile.ua/'
    pars_categories = parser_artmobile.pars_categories(url)
    print('Кількість категорій:', len(pars_categories))

r'''
Резюме:

    Питання з ДЗ4:
        У файлі interface маємо не підсвічений імпорт "from tools ...". 
        З однієї сторони втрачаємо явність з іншої оптимізація коду.
        
    Рішення:
        Імпортував модуль а не окремі функції та виконав виклик getattr(tools, func_name)(img_array)

Результат:

переглядаємо документацію пакету imggame
Help on package imggame:

NAME
    imggame

PACKAGE CONTENTS
    game_interface
    tools

VERSION
    1.1.0

AUTHOR
    Стебельський Роман

FILE
    g:\po\prodjects\project_hw\hw_5\imggame\__init__.py

-------------------------------------
переглядаємо документацію модуля parser_artmobile
Help on module parssite.load_price in parssite:

NAME
    parssite.load_price - Модуль виконує формування прайс-листів у вигляді xml та xlsx файлів

DESCRIPTION
        Функції:
            set_catalog_to_xml - ініціює запит на вивантаження курсів валют, категорій та товарів
            з інтернет-магазину. Вивантажені дані записує в xml файл.
            set_catalog_to_xlsx - ініціює завантаження даних про товари з xml файлу.
        Вивантажені дані записує в xml файл.

FUNCTIONS
    set_catalog_to_xlsx(xml_file) -> str
        set_catalog_to_xlsx - ініціює завантаження даних про товари з xml файлу.
        Вивантажені дані записує в xml файл.

        :param xml_file: рядок, назва файлу з якого будуть вантажитись дані. Розширення файлу повинно бути xml

        :return: повертає рядок з повідомленням про результат виконання. У випадку успішного виконання
        повідомлення містить повну назву сформованого файлу.

    set_catalog_to_xml(url_site) -> str
        set_catalog_to_xml - ініціює запит на вивантаження курсів валют, категорій та товарів
        з інтернет-магазину. Вивантажені дані записує в xml файл.

        :param url_site: рядок з url адресою інтернет-магазину.

        :return: повертає рядок з повідомленням про результат виконання.
        У випадку успішного виконання повідомлення містить повну назву сформованого файлу.

FILE
    g:\po\prodjects\project_hw\hw_5\parssite\load_price.py

-------------------------------------
демонстрація роботи функції game_interface з пакету imggame модуль game_interface

        1. завантажити оригінал
        2. повернути за годинниковою стрілкою
        3. повернути проти годинникової стрілки
        4. дзеркальне відображення по горизонталі
        5. дзеркальне відображення по вертикалі
        6. зменшити 
        7. зберегти
        8. завершити без збереження
    
Вкажіть номер однієї з доступних команд:8
роботу завершено без збереження зображення
-------------------------------------
демонстрація роботи функції get_exchange_rate з пакету parssite модуль api_nbu
Курс USD: 9    41.2152
Name: Amount, dtype: float64
-------------------------------------
демонстрація роботи функції get_exchange_rate з пакету parssite модуль api_nbu
 Комплектуючі до Apple
	 Запчастини iPhone
		 Акумулятори iPhone
		 Дзвінки та вібро iPhone
		 Динаміки iPhone
		 Дисплеї iPhone
		 Задні кришки iPhone
		 Камери iPhone
		 Конектори iPhone
		 Корпус iPhone
		 Корпусні деталі iPhone
		 Сенсорні екрани iPhone
		 Скло дисплея iPhone
		 Скло камер iPhone
		 Шлейфа iPhone
	 Запчастини iPad
		 Акумулятори iPad
		 Дзвінки iPad
		 Дисплеї iPad
		 Камери iPad
		 Корпус iPad
		 Корпусні деталі iPad
		 Сенсорні екрани iPad
		 Скло дисплея iPad
		 Шлейфа iPad
	 Запчастини Apple Watch
		 Шлейфа Apple Watch
		 Корпусні деталі Apple Watch
		 Сенсорні екрани Apple Watch
		 Скло дисплея Apple Watch
		 Дисплеї Apple Watch
		 Акумулятори Apple Watch
	 Запчастини iPod
		 Запчастини iPod Touch
	 Запчастини AirPods
	 Мікросхеми Apple
 Запчастини
	 Конектори
		 Конектори sim-карти і карти пам'яті
		 Конектори дисплеїв
		 Конектори зарядки
		 Конектори клавіатур і шлейфів
		 Конектори навушників
	 Корпусні деталі
		 Бічна заглушка корпуса
		 Гвинти
		 Клавіатура
		 Рамка дисплея
		 Накладки на кнопки
		 Рамка корпусу
		 Скло камер
		 Скло дисплея
		 Стилус
		 Тримач Sim-карти і карти памяті
	 Корпус
		 Задні кришки
		 Корпус
	 Дисплеї
	 Сенсорні екрани
	 Шлейфа
	 Камери
	 Дзвінки
	 Вібродзвінки
	 Динаміки
	 Мікрофони
	 Антени
	 Мікросхеми
	 Клавіатурний модуль
	 Кнопки
	 Пилозахісні сітки
 Запчастини для MacBook
	 Запчастини MacBook
 Акумулятори
	 Акумулятори (АКБ)
 Аксесуари
	 Чохли
		 Чохли для iPhone
			 Чохли iPhone 15 Pro Max
			 Чохли iPhone 15 Pro
			 Чохли iPhone 15 Plus
			 Чохли iPhone 15
			 Чохли iPhone 14 Pro Max
			 Чохли iPhone 14 Pro
			 Чохли iPhone 14 Plus
			 Чохли iPhone 14
			 Чохли iPhone 13 Pro Max
			 Чохли iPhone 13 Pro
			 Чохли iPhone 13 mini
			 Чохли iPhone 13
			 Чохли iPhone 12 Pro Max
			 Чохли iPhone 12 mini
			 Чохли iPhone 12/12 Pro
			 Чохли iPhone 11 Pro Max
			 Чохли iPhone 11 Pro
			 Чохли iPhone 11
			 Чохли iPhone XS Max
			 Чохли iPhone X/XS
			 Чохли iPhone XR
			 Чохли iPhone 7 Plus/8 Plus
			 Чохли iPhone 7/8/SE 2020
			 Чохли iPhone 6 Plus/6S Plus
			 Чохли iPhone 6/6S
			 Чохли iPhone 5/5S/SE
		 Чохли для iPad
			 Чохли iPad 2022 10th
			 Чохли iPad mini 6
			 Чохли iPad Pro 12.9 2020/2021
			 Чохли iPad Pro 11 2020
			 Чохли iPad Pro 10.5/iPad Air 3
			 Чохли iPad 7/8 10.2 2019/2020
			 Чохли iPad Pro 12.9 2018
			 Чохли iPad Pro 11 2018
			 Чохли iPad 9.7 2018/2017
			 Чохли iPad Pro 12.9 2017
			 Чохли iPad Pro 9.7
			 Чохли iPad Air 2
			 Чохли iPad Air
			 Чохли iPad mini 5
			 Чохли iPad mini 2/3/4
			 Чохли iPad 2/3/4
			 Чохли iPad
		 Чохли для Macbook
		 Чохли для Apple Watch
		 Чохли для AirPods
		 Чохли для Airtag
		 Чохли для Samsung
		 Чохли для Xiaomi
		 Чохли для Huawei
	 Ремінці Apple Watch
		 Ремінці 42/44/45/49mm
		 Ремінці 38/40/41mm
	 Зарядні пристрої
		 Macbook (Блоки живлення)
		 Бездротові зарядки
		 Мережеві (адаптери)
	 Фітнес-браслети і ремінці
	 Кабелі зарядки
	 Хаби і перехідники
	 Навушники і колонки
	 Продукція Xiaomi
	 Автоаксесуари
	 Фотографія та відео
	 Клавіатури та миші, стілуси
	 Зовнішні акумулятори
	 Сумки
 Захисні плівки та скло
	 Захисне скло iPhone
		 Захисне скло iPhone 16 Pro Max
		 Захисне скло iPhone 16 Pro
		 Захисне скло iPhone 16
		 Захисне скло iPhone 15 Pro Max
		 Захисне скло iPhone 15 Pro
		 Захисне скло iPhone 14 Pro Max/15 Plus
		 Захисне скло iPhone 14 Pro/15
		 Захисне скло iPhone 13 Pro Max/14 Plus
		 Захисне скло iPhone 13/13 Pro/14
		 Захисне скло iPhone 13 mini
		 Захисне скло iPhone 12 Pro Max
		 Захисне скло iPhone 12/12 Pro
		 Захисне скло iPhone 12 mini
		 Захисне скло iPhone XR/11
		 Захисне скло iPhone XS Max/11 Pro Max
		 Захисне скло iPhone X/XS/11 Pro
		 Захисне скло iPhone 7 Plus/8 Plus
		 Захисне скло iPhone 7/8/SE2020
		 Захисне скло iPhone 6 Plus/6S Plus
		 Захисне скло iPhone 6/6S
	 Захисне скло iPad
	 Захисне скло Apple Watch
	 Захисне скло Macbook
	 Захисне скло Android
	 Захисні плівки iPhone
		 Захисна плівка iPhone 15 Pro Max
		 Захисна плівка iPhone 15 Pro
		 Захисна плівка iPhone 14 Pro Max
		 Захисна плівка iPhone 14 Pro
		 Захисна плівка iPhone 13 Pro Max/14 Plus
		 Захисна плівка iPhone 13/13 Pro/14
		 Захисна плівка iPhone 13 mini
		 Захисна плівка iPhone 12 Pro Max
		 Захисна плівка iPhone 12/12 Pro
		 Захисна плівка iPhone 12 mini
		 Захисна плівка iPhone XR/11
		 Захисна плівка iPhone XS Max/11 Pro Max
		 Захисна плівка iPhone X/XS/11 Pro
		 Захисна плівка iPhone 7/8/SE 2020/SE 2022
		 Захисна плівка iPhone 7 Plus/8 Plus
		 Захисна плівка iPhone 6 Plus/6S Plus
		 Захисна плівка iPhone 6/6S
		 Захисна плівка iPhone 4/4S
		 Захисна плівка iPhone 3G/3GS
	 Захисні плівки iPad
	 Захисні плівки Apple Watch
	 Захисні плівки Macbook
	 Захисні плівки iPod
	 Захисні плівки Android
 Обладнання для ремонту техніки
	 Обладнання для ремонту
		 Інструменти для ремонту
		 Обладнання для паяння
	 Витратні матеріали
		 Хімія та витратні матеріали
		 Клей
		 Скотчі
		 OCA плівки
		 Поляризаційні плівки
 Уцінка
	 Уцінка
Кількість категорій: 208

Process finished with exit code 0

'''