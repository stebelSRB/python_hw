# --------------------------- Homework_3  ------------------------------------

'''

Виконав: Роман Стебельський
Homework_3, ІI рівень складності:

Група вимог І
    Файли формується двох типів на власний вибір. Формування файлів має
    здійснюватися з використанням операторів з переліку: умовних (if, elif, else), циклічних
    (while і for) вибору (matching). Файл CV має бути належним чином відформатований (рядки,
    пробіли, знаки пунктуації).
Група вимог ІІ
    Формування файлів пропонується супроводжується застосуванням технології
    обробки винятків (виключень): try / except / else / finally.

Алгоритм реалізує:
    1. Зчитування актуальних курсів валют з API НБУ
    2. Парсинг даних (дерево категорій та товари) з сайту https://artmobile.ua/.
    Під час виконання парсингу відбувається вивід на екран дерева каталогу та логування проаналізованих сторінок з товарами.
    3. Виконує запис отриманих даних з web ресурсів в xml файл
    4. Вичитує частину даних з xml файлу та записує їх в xlsx файл

Package                      Version
---------------------------- -----------
pip                          23.2.1
requests                     2.32.3
bs4                          0.0.2
lxml                         5.3.2
pandas                       2.2.3

'''

# ------------------------ парсинг сайту ----------------------------
import requests
import time
from bs4 import BeautifulSoup as bs
from lxml import etree
import pandas as pd
from io import StringIO

def get_html_site(url) ->str:

    '''
    get_html_site - виконує запит до web ресурсу та повертає результат у вигляді str.

    :param url: рядок з url адресою web ресурсу.

    :return:
        у випадку успіху - повертає результат у вигляді str
        у випадку помилки - порожній str
    '''

    result = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    time.sleep(0.5)
    try:
        result_requests = requests.get(url, headers=headers)
        if result_requests.status_code == 200:
            result = result_requests.text

    except requests.exceptions.ConnectionError:
        print('Помилка запиту  до web ресурсу -', url)
    finally:
        return result

def get_exchange_rate(currencies: 'list' = list):

    '''
    get_exchange_rate - виконує запит до API НБУ та повертає перелік валют з актуальним курсом.

    :param currencies: список, кожен елемент котрого містить рядок з літеральним кодом валюти, наприклад ['USD'].
    Застосовується для виконання фільтрації за полем CurrencyCodeL.
    За замовченням порожній список.
    :return:
        у випадку успіху - DataFrame з даними про курс валют. поля: StartDate, TimeSign, CurrencyCode, CurrencyCodeL, Units, Amount
        у випадку помилки - NoneType
    '''

    result = None
    url = 'https://bank.gov.ua/NBU_Exchange/exchange?json'
    site_str = get_html_site(url)

    try:
        site_str = StringIO(site_str)
        result = pd.read_json(site_str)
        if currencies:
            result = result[result['CurrencyCodeL'].isin(currencies)]
    except (ValueError, KeyError):
        print('Результат запиту до API НБУ неможливо обробити')
    finally:
        return result

def pars_categories(url: 'str', parent_id: 'str' = '', level_category: 'int' = 0) ->list:

    '''
    pars_categories - виконує парсинг категорій товарів інтернет-магазину, рекурсивно перебирає дочірні категорії.

    :param url: рядок з url адресою інтернет-магазину.

    :param parent_id: рядок містить текстовий ідентифікатор батьківської категорії.
    За замовченням порожній рядок.

    :param level_category: ціле число вказує на рівень віддаленості категорії від головної батьківської категорії.
    За замовченням дорівнює 0.

    :return:
        у випадку успіху - список з даними категорій, де кожен елемент є словником з наступною структурою:
            {'id': str, 'title': str, 'href': str, 'parent_id': str, 'level_category': int, 'sub_count': int}
        у випадку помилки - порожній список
    '''

    result = []
    data_site = get_html_site(url)
    data_site = bs(data_site, "html.parser")

    if data_site:
        if parent_id == '':
            categories = data_site.select("ul.lv-1 > li")
        else:
            categories = data_site.select("div.catalog-aside > div.catalog-aside-item")

        for category in categories:
            try:
                title = category.a['title']
                href = category.a['href']
                category_id = href[len(url):].strip('-')
                print('\t' * level_category, title)

                result.append({
                    'id': category_id,
                    'title': title,
                    'href': href,
                    'parent_id': parent_id,
                    'level_category': level_category,
                    'sub_count': 0,
                })

                if category.ul is not None:
                    sub_categories = pars_categories(href, category_id, level_category + 1)
                    result[len(result) - 1]['sub_count'] = len(sub_categories)
                    result += sub_categories

            except (KeyError, TypeError):
                print('За посиланням', url, 'атрибут або тег категорії не знайдено.')
                break

    return result

def pars_offers(categories) ->list:

    '''
    pars_offers - виконує парсинг товарів інтернет-магазину.

    :param categories: список з даними категорій, де кожен елемент є словником з наступною структурою:
            {'id': str, 'title': str, 'href': str, 'parent_id': str, 'level_category': int, 'sub_count': int}

    :return:
        у випадку успіху - список з даними товарів, де кожен елемент є словником з наступною структурою:
            {'id': str, 'category_id': str, 'title': str, 'href': str, 'img': str, 'price': float, 'available': str, 'currencyId': str}
        у випадку помилки - порожній список
    '''

    result = []

    for category in categories:

        if category['sub_count'] != 0:
            continue

        # ця умова додана виключно для зменшення часу роботи скрипту під час демонстрації
        if category['parent_id'] != 'obladnannya-dlya-remontu' and category['parent_id'] != 'vitratni-materiali':
            continue
        # ця умова додана виключно для зменшення часу роботи скрипту під час демонстрації

        category_id = category['id']
        page = 1
        while page > 0:

            print('pars page -', page, 'from category -',  category['title'])
            current_url = category['href'] + '?page=' + str(page)
            data_site = get_html_site(current_url)
            data_site = bs(data_site, "html.parser")

            if data_site:

                offers = data_site.select("div.catalog-list-more > div.product-card-wrapper > div.product-card")

                for offer in offers:
                    try:
                        title = offer.a['title']
                        href = offer.a['href']
                        img = offer.a.picture.img['src']
                        price = offer.find('span', class_='price-value').\
                            get_text(strip=True)
                        stock = offer.find('div', class_='stock-info').\
                            get_text(strip=True).\
                            replace('\xa0', ' ')

                        result.append({
                            'id': offer['data-product'],
                            'category_id': category_id,
                            'title': title,
                            'href': href,
                            'img': img,
                            'price': float(price),
                            'available': 'true' if stock == 'В наявності' else 'false',
                            'currency_id': 'USD'
                        })
                    except (AttributeError, KeyError, TypeError):
                        print('За посиланням', current_url, 'атрибут або тег товару не знайдено.')
                        break
                    except ValueError:
                        print('За посиланням', current_url, 'неможливо виконати перетворення ціни в формат float.')

                check_finish = data_site.select('ul.pagination > li.page-item > a.page-next')
                if len(check_finish) == 0 :
                    break
                page += 1

    return result

def set_catalog_to_xml(url_site) -> str:

    '''
    set_catalog_to_xml - ініціює запит на вивантаження курсів валют, категорій та товарів з інтернет-магазину.
    Вивантажені дані записує в xml файл.

    :param url_site: рядок з url адресою інтернет-магазину.

    :return: повертає рядок з повідомленням про результат виконання. У випадку успішного виконання повідомлення містить повну назву сформованого файлу.
    '''

    result = ''
    print('Завантажується курс валют')
    print('-----------------------------')
    currencies_list = ['USD', 'EUR']
    exchange_rate = get_exchange_rate(currencies_list)
    print('Виконується парсинг категорій')
    print('-----------------------------')
    categories_data = pars_categories(url_site)
    print('Виконується парсинг товарів')
    print('-----------------------------')
    offers_data = pars_offers(categories_data)

    shop = etree.Element('shop')
    etree.SubElement(shop, 'name').text = 'artmobile'
    etree.SubElement(shop, 'company').text = 'artmobile'
    etree.SubElement(shop, 'url').text = url_site
    etree.SubElement(shop, 'version').text = '1.5.5.1.2'

    currencies = etree.SubElement(shop, 'currencies')
    try:
        for index, val in exchange_rate.iterrows():
            etree.SubElement(currencies, 'currency', id=val['CurrencyCodeL'], rate=str(val['Amount']))

        categories = etree.SubElement(shop, 'categories')
        for val in categories_data:
            category = etree.SubElement(categories, 'category', id=val['id'])
            if val['parent_id']:
                category.set('parent_id', val['parent_id'])
            category.text = val['title']

        offers = etree.SubElement(shop, 'offers')
        for val in offers_data:
            offer = etree.SubElement(offers, 'offer', id=val['id'], available=val['available'])
            del val['id']
            del val['available']
            for key, v in val.items():
                etree.SubElement(offer, key).text = str(v)
    except (AttributeError, KeyError, TypeError):
        result ='Не вдалось виконати завис валют/категорій/товарів в xml файл'
    else:
        tree = etree.ElementTree(shop)
        dst = time.localtime()
        dst = time.strftime("%Y-%m-%d_%H%M%S", dst)
        file_name = 'artmobile_price (' + dst + ').xml'
        with open(file_name, "wb") as file:
            tree.write(file, pretty_print=True, xml_declaration=True, encoding="utf-8")
        result = file_name
    finally:
        return result

def set_catalog_to_xlsx(xml_file) -> str:

    '''
    set_catalog_to_xlsx - ініціює завантаження даних про товари з xml файлу.
    Вивантажені дані записує в xml файл.

    :param xml_file: рядок, назва файлу з якого будуть вантажитись дані. Розширення файлу повинно бути xml

    :return: повертає рядок з повідомленням про результат виконання. У випадку успішного виконання повідомлення містить повну назву сформованого файлу.
    '''

    result = ''
    try:
        df = pd.read_xml(xml_file, xpath=".//offer")
    except (etree.XMLSyntaxError, UnicodeDecodeError):
        result = 'Виконати зчитування файлу ' + xml_file + ' не вдалось'
    except ValueError:
        result = 'Виконати парсинг файлу ' + xml_file + ' не вдалось'
    else:
        dst = time.localtime()
        dst = time.strftime("%Y-%m-%d_%H%M%S", dst)
        xlsx_file =  'artmobile_price (' + dst + ').xlsx'
        df.to_excel(xlsx_file, index=False)
        result = xlsx_file
    finally:
        return result

if __name__ == '__main__':

    start_p = time.time()


    # парсинг сайту та запис результату в xml файл
    url_site = 'https://artmobile.ua/'
    result_func_run = set_catalog_to_xml(url_site)
    print('Результат виконання set_catalog_to_xml:', result_func_run)

    # Вичитує частину даних з xml файлу та записує їх в xlsx файл
    file_name = 'artmobile_price (2025-04-08_101203).xml'
    result_func_run = set_catalog_to_xlsx(file_name)
    print('Результат виконання set_catalog_to_xlsx:', result_func_run)

    time_p = time.time() - start_p
    time_p_str = time.strftime('%H:%M:%S', time.gmtime(time_p))
    print('час виконання:', time_p_str)

'''

Резюме:
1. У функції pars_offers поставив "заглушку" (рядок 175). 
Ця умова додана виключно для зменшення часу роботи скрипту під час демонстрації. Час виконання скрипту приблизно 1 хв.
Час парсингу усього сайту приблизно 30 хв - artmobile_price (all).xml
2. У get_html_site перед запитом до ресурсу використовується time.sleep(0.5) - для зменшення навантаження на ресурс який парситься.
3. Імпортував StringIO, так як отримував повідомлення
FutureWarning: Passing literal xml to 'read_xml' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object.
4. Питання. Функція get_exchange_rate в залежності від успішності виконання може повернути як pandas.core.frame.DataFrame так і NoneType.
Як краще зробити у цьому випадку створити порожній DataFrame і явно вказати який тип повертає функція ->DataFrame? 
Але є відчуття що у такому випадку буде зайве навантаження системи при тому ж результаті

Результат:

Завантажується курс валют
-----------------------------
Виконується парсинг категорій
-----------------------------
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
Виконується парсинг товарів
-----------------------------
pars page - 1 from category - Інструменти для ремонту
pars page - 2 from category - Інструменти для ремонту
pars page - 3 from category - Інструменти для ремонту
pars page - 4 from category - Інструменти для ремонту
pars page - 5 from category - Інструменти для ремонту
pars page - 6 from category - Інструменти для ремонту
pars page - 7 from category - Інструменти для ремонту
pars page - 8 from category - Інструменти для ремонту
pars page - 1 from category - Обладнання для паяння
pars page - 2 from category - Обладнання для паяння
pars page - 3 from category - Обладнання для паяння
pars page - 4 from category - Обладнання для паяння
pars page - 1 from category - Хімія та витратні матеріали
pars page - 1 from category - Клей
pars page - 1 from category - Скотчі
pars page - 2 from category - Скотчі
pars page - 1 from category - OCA плівки
pars page - 2 from category - OCA плівки
pars page - 3 from category - OCA плівки
pars page - 4 from category - OCA плівки
pars page - 5 from category - OCA плівки
pars page - 6 from category - OCA плівки
pars page - 1 from category - Поляризаційні плівки
pars page - 2 from category - Поляризаційні плівки
Результат виконання set_catalog_to_xml: artmobile_price (2025-04-08_101203).xml
Результат виконання set_catalog_to_xlsx: artmobile_price (2025-04-08_101203).xlsx
час виконання: 00:01:03

Process finished with exit code 0



'''
