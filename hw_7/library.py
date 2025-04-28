
'''
У цьому модулі описаний клас який організовує бібліотеку книжок,

Клас надає інструменти для додавання/видалення пошуку книг, а також
виконує валідацію вхідних даних
'''

from typing import TypedDict
from pydantic import BaseModel, ValidationError

class library_st_valid(TypedDict):

    '''
    клас забезпечує валідацію атрибутів книги у вигляді підказок від IDE
    '''

    author: str
    title: str
    publisher: str
    genre: str
    year_publication: int

class library_rt_valid(BaseModel):

    '''
    клас забезпечує валідацію атрибутів книги під час виконання коду
    '''
    author: str
    title: str
    publisher: str
    genre: str
    year_publication: int

class library():

    '''
    клас організовує бібліотеку книжок, та надає інструменти для роботи з нею
    '''

    def __init__(self, key: int, lib_data: library_st_valid):

        self.items: dict[int, library_st_valid] = {}
        self.__setitem__(key, lib_data)

    def __setitem__(self, key: int, lib_data: library_st_valid):

        if key in self:
            print('книга під номером', key, 'вже існує')
        else:
            try:
                validated = library_rt_valid(**lib_data)
                self.items[int(key)]: dict[str, str, str, str, int] = {
                    'author': validated.author,
                    'title': validated.title,
                    'publisher': validated.publisher,
                    'genre': validated.genre,
                    'year_publication': validated.year_publication,
                }
                print('книгу', '"'+validated.title+'"', 'додано до бібліотеки')
            except (ValidationError, ValueError):
                print('дані про книгу неповні або некоректні')

    def __contains__(self, key: int) -> bool:
        return key in self.items

    def __getitem__(self, key: int) -> library_st_valid | None:
        if key in self.items:
            return self.items[key]
        else:
            print('книги з вказаним номером не знайдено')

    def __delitem__(self, key: int) -> None:
        if key in self.items:
            del self.items[key]
            print('книгу під номером -', key, 'видалено')
        else:
            print('книги з вказаним номером не знайдено')

    def __iter__(self):
        return iter(self.items)

    def __call__(self, *, author=None, title = None, publisher = None, genre = None, year_publication = None) -> dict[int, library_st_valid]:
        result = {}
        for item_id, item in self.items.items():
            if (
                    (author is None or item['author'] == author) and
                    (title is None or item['title'] == title) and
                    (publisher is None or item['publisher'] == publisher) and
                    (genre is None or item['genre'] == genre) and
                    (year_publication is None or item['year_publication'] == year_publication)
            ):
                result[item_id] = item
        return result

    def __del__(self):
        print('бібліотека зачиняється.')