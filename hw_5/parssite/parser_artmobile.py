'''
    Модуль виконує парсинг сайту https://artmobile.ua/

    Функції:
        pars_categories - виконує парсинг категорій товарів інтернет-магазину,
        рекурсивно перебирає дочірні категорії.
        pars_offers - виконує парсинг товарів інтернет-магазину.
'''

from bs4 import BeautifulSoup as bs
from .http_request import get_html_site

#------------------------- опис функцій ---------------------------------
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
