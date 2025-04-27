# --------------------------- Homework_1  ------------------------------------

'''

Виконав: Роман Стебельський
Homework_1, ІI рівень складності:
Розробити python програмний скрипт, який реалізує перелік технічних вимог І, ІІ.
Група вимог І
Здійснити програмний розрахунок площі пласких (2D) фігур за власним вибором,
параметри фігури вводити із клавіатури. Результат привести до обраного простого типу з
переліку: numeric (int, float), str.
    Алгоритм реалізує:
        1. визначення переліку фігур та їх атрибутів. Кожна фігура має наступні атрибути:
            name - назва
            result_caption - підпис який передує значенню площі при виведенні результату
            input - перелік параметрів для вводу. ключ - назва змінної параметру, значення - підпис повідомлення при зборі даних
        2. вибір однієї з фігур (коло, прямокутник, трапеція)
        3. визначення переліку вхідних параметрів відповідно до обраної фігури
        4. введення вхідних параметрів
        5. визначення алгоритму розрахунку площі відповідно до обраної фігури
        6. розрахунок площі фігури
        7. виведення результату
Група вимог ІІ
Сформувати електронну форму власного CV з використанням 3 типів структур даних з переліку: list, tuple, set, dict, array.
    Алгоритм реалізує:
        1. визначення функції візуалізації CV:
            1. визначення рядка результату
            2. запис caption в рядок результату
            3. запис результату:
                3.1 запис результату рекурсії в рядок результату якщо val має тип list
                3.2 запис декількох значень val в рядок результату якщо val має тип set або tuple
                3.3 запис val в рядок результату якщо val не має тип set, tuple, list
            4 виведення рядка результату

        2. визначення CV яке являє сбою перелік атрибутів співробітника та представлене у вигляді типу даних list.
        Кожен атрибут представлений у вигляді типу даних dictionary котрий має два елементи з ключами caption та val де:
            caption: підпис/назва атрибута тип даних - string
            val: значення атрибута, яке може бути:
                - атрибут має одне значення, тип даних не list/set/tuple/array
                - атрибут має декілька значень, тип даних:
                    set - якщо порядок відображення не важливий,
                    tuple - якщо порядок відображення має значення,
                    array - для випадків коли значення атрибута надані у вигляді list, але виконання рекурсії не потрвбне
                - атрибути має значення у вигляді окремого переліку атрибутів (sub_cv), тип даних list

        3. формування рядка візуалізації CV
        4. вивід CV на екран
Група вимог ІІI
Розробити блок-схему алгоритму для реалізації технічних вимог груп І, ІІ в середовищі https://www.diagrams.net/
    Група вимог І - https://drive.google.com/file/d/1JQnuLcFlg4vcinfof0KzwemUTpPPeyvR/view?usp=sharing
    Група вимог ІІ - https://drive.google.com/file/d/1iZzg353TMSV50l7IqDKip8QPIDzCosm7/view?usp=sharing

Package                      Version
---------------------------- -----------
pip                          23.2.1
numpy                        2.2.4

'''


# --------------------------------- група вимог І ----------------------------------------------
# 1. визначення переліку фігур та їх атрибутів
figures = {
    1: {
        'name': 'коло',
        'result_caption': 'площа кола',
        'input': {
            'r': 'радіус кола - '
        }
    },
    2: {
        'name': 'прямокутник',
        'result_caption': 'площа прямокутника',
        'input': {
            'a': 'довжину прямокутника - ',
            'b': 'ширину прямокутника - '}
        },
    3: {
        'name': 'трапеція',
        'result_caption': 'площа трапеції',
        'input': {
            'a': 'першу основу трапеції - ',
            'b': 'другу основу трапеції - ',
            'h': 'висоту трапеції - '
        }
    }
}
msg_result       = ''
s_figure         = 0
selected_figure  = 0
output_parameter = dict()

try:
    # 2. вибір однієї з фігур (коло, прямокутник, трапеція)
    print('Вкажіть номер фігури площу котрої необхідно розрахувати:')
    for key in figures:
        print(key, '). ', figures[key]['name'], sep='')

    selected_figure = int(input('номер фігури - '))

    # 3. визначення переліку вхідних параметрів відповідно до обраної фігури
    input_parameter =  figures[selected_figure]['input']
except ValueError:
    msg_result = 'Визначити фігуру не вдалось. Вкажіть ціле число від 1 до ' + str(len(figures))
except KeyError:
    msg_result = 'Фігура за введеним числом не закріплена. Вкажіть число від 1 до ' + str(len(figures))

if len(msg_result) == 0:

    # 4. введення вхідних параметрів відповідно до обраної фігури
    print('ви обрали фігуру -', figures[selected_figure]['name'])
    print('вкажіть параметр(и) фігури')
    try:
        for key in input_parameter:
            output_parameter[key] = float(input(input_parameter[key]))

        # 5. визначення алгоритму розрахунку площі відповідно до обраної фігури
        match selected_figure:
            case 1:
                # 6.1 розрахунок площі кола
                r = output_parameter['r']
                s_figure = 3.14 * r * r
            case 2:
                # 6.2 розрахунок площі прямокутника
                a, b = output_parameter.values()
                s_figure = a * b
            case 3:
                # 6.3 розрахунок площі трапеції
                a, b, h = output_parameter.values()
                s_figure = (a + b) * 0.5 * h
            case _:
                pass

        msg_result = figures[selected_figure]['result_caption'] + ' - ' + str(s_figure)
    except ValueError:
        msg_result = 'один або декілька параметрів фігури не відповідають вимогам. введіть число'

# 7. виведення результату
print(msg_result)


# --------------------------------- група вимог ІI ----------------------------------------------
# імпорт бібліотеки
import numpy

# 1. оголошення функції show_cv
def show_cv(data_set, tab = ''):

    # 1. визначення рядка результату
    result_str = ''
    for x in data_set:

        # 2. запис caption в рядок результату
        result_str += tab + x['caption'] + ':'
        if type(x['val']) == list:

            # 3.1 запис результату рекурсії в рядок результату якщо val має тип list
            result_str +=  '\n' + show_cv(x['val'], tab + '\t')
        elif type(x['val']) in (set, tuple, numpy.ndarray):

            # 3.2 запис декількох значень val в рядок результату якщо val має тип set або tuple
            result_str += '\n'
            for y in x['val']:
                result_str += tab + '\t- ' + str(y) + '\n'
        else:

            # 3.3 запис val в рядок результату якщо val не має тип set, tuple, list
            result_str += ' ' + str(x['val']) + ' \n'

    # 4. виведення рядка результату
    return result_str

# 2.1 визначення значень атрибутів hobbies, job_duties
hobbies    = {'football', 'tennis', 'radio models', 'fishing'}
job_duties = ['analytics', 'script development', 'report generation']
job_duties = numpy.array(job_duties)

# 2.2 визначення значень атрибутів set_processes. Який є sub_cv для technical_skills
set_processes = [
    {
        'caption': 'Power Automate',
        'val': {'process is automated - 1', 'process is automated - 2', 'process is automated - 3', 'process is automated - 4' }
    },
    {
        'caption': 'API integration',
        'val': {'process is automated - 2', 'process is automated - 6'}
    }
]

# 2.3 визначення значень атрибутів technical_skills. Який є sub_cv для my_cv
technical_skills = [
    {
        'caption': 'programming languages',
        'val': ('PHP (framework kohana)', 'VBA', 'Python (basics)')
    },
    {
        'caption': 'working with databases',
        'val': ('my sql', 'MS server',  'PrestoDB (AWS Athena)',  'PySpark')
    },
    {
        'caption': 'visualization of reports',
        'val': 'Power BI'
    },
    {
        'caption': 'process automation',
        'val': set_processes
    }
]

# 2.4 визначення значень атрибутів my_cv
my_cv = [
    {
        'caption': 'name',
        'val': 'Roman Stebelskiy'
    },
    {
        'caption': 'birtn',
        'val': '17.07.1988'
    },
    {
        'caption': 'age',
        'val': 36
    },
    {
        'caption': 'hobbies',
        'val': hobbies
    },
    {
        'caption': 'job duties',
        'val': job_duties
    },
    {
        'caption': 'technical skills',
        'val': technical_skills
    }
]

# 3. формування рядка візуалізації CV
result_str = show_cv(my_cv)

# 4. вивід CV на екран
print(result_str)