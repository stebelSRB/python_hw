
'''
Модуль для роботи з API НБУ.

Модуль містить функцію яка виконує запит до API НБУ та повертає
перелік валют з актуальним курсом. До цього модуля можливо додавати
додаткові функції які будуть взаємодіяти з API НБУ.
'''

import pandas as pd
from io import StringIO
from .http_request import get_html_site

#------------------------- опис функцій ---------------------------------
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
