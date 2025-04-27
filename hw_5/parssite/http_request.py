
'''
Модуль для виконання http запитів до web ресурсів.

Модуль містить функцію яка виконує запит до web ресурсу та повертає
результат у вигляді str. До цього модуля можливо додавати
додаткові функції які будуть модифікувати результат http запиту
та повертати результат у вигляді json і т.п.
'''

import requests
import time

#------------------------- опис функцій ---------------------------------
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
