'''
модуль з календарем

'''

import calendar
import locale

# встановлюємо базові налаштування
my_locale = locale.getlocale()
locale.setlocale(locale.LC_ALL, my_locale)
new_locale = {'new_locale': 'de_DE.utf8'}

def translate(my_locale: str | tuple, new_locale: dict):

    '''
    тимчасово змінює локалізацію

    :param my_locale: локалізація сервера (не змінюється після того як функція задекорована)
    :param new_locale: цільова локалізація (змінюється після того як функція задекорована)
    :return: обгорнуту функію
    '''

    def wrapper_transl(func):
        def wrapper(**kwargs):
            locale.setlocale(locale.LC_ALL, new_locale['new_locale'])
            func(**kwargs)
            locale.setlocale(locale.LC_ALL, my_locale)
        return wrapper
    return wrapper_transl

def short_form(func):
    def wrapper(**kwargs):
        # цільовий перелік днів
        list_day = func(**kwargs)
        # повний перелік днів, для визначення номера дня
        all_list_day = func()
        # коротка назва
        short_list_day = list(calendar.day_abbr[all_list_day.index(cap_day)] for cap_day in list_day)
        print('перелік днів з функції', short_list_day)
    return wrapper

@translate(my_locale, new_locale)
@short_form
def get_data(start: int = None, finish: int = None) -> list:
    return list(calendar.day_name)[start:finish]
