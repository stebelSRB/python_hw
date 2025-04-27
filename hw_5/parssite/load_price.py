
'''
Модуль виконує формування прайс-листів у вигляді xml та xlsx файлів

    Функції:
        set_catalog_to_xml - ініціює запит на вивантаження курсів валют, категорій та товарів
        з інтернет-магазину. Вивантажені дані записує в xml файл.
        set_catalog_to_xlsx - ініціює завантаження даних про товари з xml файлу.
        Вивантажені дані записує в xml файл.
'''

import time
from lxml import etree
import pandas as pd
from .api_nbu import get_exchange_rate
from . import parser_artmobile as pa

#------------------------- опис функцій ---------------------------------
def set_catalog_to_xml(url_site) -> str:

    '''
    set_catalog_to_xml - ініціює запит на вивантаження курсів валют, категорій та товарів
    з інтернет-магазину. Вивантажені дані записує в xml файл.

    :param url_site: рядок з url адресою інтернет-магазину.

    :return: повертає рядок з повідомленням про результат виконання.
    У випадку успішного виконання повідомлення містить повну назву сформованого файлу.
    '''

    result = ''
    print('Завантажується курс валют')
    print('-----------------------------')
    currencies_list = ['USD', 'EUR']
    exchange_rate = get_exchange_rate(currencies_list)
    print('Виконується парсинг категорій')
    print('-----------------------------')
    categories_data = pa.pars_categories(url_site)
    print('Виконується парсинг товарів')
    print('-----------------------------')
    offers_data = pa.pars_offers(categories_data)

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

    :return: повертає рядок з повідомленням про результат виконання. У випадку успішного виконання
    повідомлення містить повну назву сформованого файлу.
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

