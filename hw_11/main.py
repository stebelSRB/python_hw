# --------------------------- Homework_11  ------------------------------------

r'''

Виконав: Роман Стебельський
Homework_11

    Завдання_1. З використанням технології стека – stack та рекурсивних викликів
    розробити програмний скрипт алгоритму «Ханойська вежа»
    (https://www.geeksforgeeks.org/python-program-for-tower-of-hanoi/).
    Алгоритм «Ханойська вежа»:
    Для піраміди із 3 веж - стрижнів необхідно перемістити всі диски на сусідній стрижень
    з урахуванням наступних правил:
    1. За один крок переміщається тільки один диск;
    2. Диск більшого розміру не можна розташовувати над диском меншого розміру.
    За опорне рішення можливо взяти скрипт my_stack_collections.py.
    
    Завдання_2. З використанням технології черги – queue організувати модель обробки
    потоку звернень до сервера (back-end) від множини клієнтів (front-end). Тобто маємо
    ситуацію обробки декількох черг. В якості алгоритму рішення рекомендується розглянути
    сценарії: «черга – черг», «стек – черг», «черга / стек з пріоритетами».
    За опорне рішення можливо взяти скрипт queue_with_stream.py.
    
    Завдання_4. Розробити граф Вашого найпопулярнішого переміщення містом з
    альтернативами маршрутів, де вузли – реперні точки, наприклад головні перехрестя, а дуги
    – відстані + час подолання відстані (пропорційно до завантаженню трафіка руху).
    Розробити програмний скрипт обчислення оптимального маршруту за мінімумом суми
    значень дуг графа (відстань+час).
    За опорне рішення взяти скрипт graph_3.py.




'''

import tower_of_hanoi as th
import client_server as cs
from graph import Graph
# ---------------------------------- головні виклики --------------------------------
if __name__ == "__main__":

    print('--------------------------- tower_of_hanoi ---------------------------')
    th.run_calculation(4)

    print('---------------------------  back-end request front-end ---------------------------')
    cs.demo_client_server()

    print('---------------------------  пошук маршруту ---------------------------')

    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 7, 5)
    g.add_edge('a', 'c', 9, 11)
    g.add_edge('a', 'f', 14, 10)
    g.add_edge('b', 'c', 10, 4)
    g.add_edge('b', 'd', 15, 8)
    g.add_edge('c', 'd', 11, 3)
    g.add_edge('c', 'f', 2, 4)
    g.add_edge('d', 'e', 6, 2)
    g.add_edge('e', 'f', 9, 4)    

    # Редагування параметрів ребра
    g.get_vertex('a').edit_param(g.get_vertex('b'), 'distance', 9)

    # Відображення ребер графа
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print(f'{vid} -> {wid}, weight: {v.get_params(w)}')

    # встановлення пріоритетів параметрів маршруту
    g.set_priorites_param_to_route('duration', 2)

    # Рекурсивнтий пошук маршруту  
    print('Пошук маршруту з використанням рекурсії:')
    print(g.search_route_recursion('a', 'e'))
    # Пошук маршруту з використанням черги
    print('Пошук маршруту з використанням черги:')
    print(g.search_route_queue('a', 'e'))



r'''    

Результат:

Initial state of Tower of Hanoi:
{'source': deque([4, 3, 2, 1]), 'destination': deque([]), 'auxiliary': deque([])}
Starting Tower of Hanoi with 4 disks...
{'source': deque([4, 3, 2]), 'destination': deque([]), 'auxiliary': deque([1])}
{'source': deque([4, 3]), 'destination': deque([2]), 'auxiliary': deque([1])}
{'source': deque([4, 3]), 'destination': deque([2, 1]), 'auxiliary': deque([])}
{'source': deque([4]), 'destination': deque([2, 1]), 'auxiliary': deque([3])}
{'source': deque([4, 1]), 'destination': deque([2]), 'auxiliary': deque([3])}
{'source': deque([4, 1]), 'destination': deque([]), 'auxiliary': deque([3, 2])}
{'source': deque([4]), 'destination': deque([]), 'auxiliary': deque([3, 2, 1])}
{'source': deque([]), 'destination': deque([4]), 'auxiliary': deque([3, 2, 1])}
{'source': deque([]), 'destination': deque([4, 1]), 'auxiliary': deque([3, 2])}
{'source': deque([2]), 'destination': deque([4, 1]), 'auxiliary': deque([3])}
{'source': deque([2, 1]), 'destination': deque([4]), 'auxiliary': deque([3])}
{'source': deque([2, 1]), 'destination': deque([4, 3]), 'auxiliary': deque([])}
{'source': deque([2]), 'destination': deque([4, 3]), 'auxiliary': deque([1])}
{'source': deque([]), 'destination': deque([4, 3, 2]), 'auxiliary': deque([1])}
{'source': deque([]), 'destination': deque([4, 3, 2, 1]), 'auxiliary': deque([])}
Final state of Tower of Hanoi:
{'source': deque([]), 'destination': deque([4, 3, 2, 1]), 'auxiliary': deque([])}
---------------------------  back-end request front-end ---------------------------
------------- черга - черг (з пріорітетом від 1 до 3 та maxsize=2) -------------
worker_back_end старт
запит № client-1_req_1 з пріорітетом - 3 від client-1 створено
запит № client-1_req_2 з пріорітетом - 2 від client-1 створено
запит № client-1_req_3 з пріорітетом - 1 від client-1 створено
запит № client-2_req_1 з пріорітетом - 3 від client-2 створено
запит № client-2_req_2 з пріорітетом - 3 від client-2 створено
запит № client-3_req_1 з пріорітетом - 3 від client-3 створено
запит № client-3_req_2 з пріорітетом - 3 від client-3 створено
запит № client-1_req_1 з пріорітетом - 3 виконано
запит № client-1_req_3 з пріорітетом - 1 виконано
запит № client-1_req_2 з пріорітетом - 2 виконано
запит № client-2_req_3 з пріорітетом - 2 від client-2 створено
запит № client-2_req_1 з пріорітетом - 3 виконано
запит № client-2_req_4 з пріорітетом - 1 від client-2 створено
запит № client-2_req_3 з пріорітетом - 2 виконано
запит № client-2_req_5 з пріорітетом - 1 від client-2 створено
запит № client-2_req_4 з пріорітетом - 1 виконано
запит № client-2_req_5 з пріорітетом - 1 виконано
запит № client-2_req_2 з пріорітетом - 3 виконано
запит № client-3_req_3 з пріорітетом - 1 від client-3 створено
запит № client-3_req_1 з пріорітетом - 3 виконано
запит № client-3_req_4 з пріорітетом - 2 від client-3 створено
запит № client-3_req_3 з пріорітетом - 1 виконано
запит № client-3_req_5 з пріорітетом - 2 від client-3 створено
запит № client-3_req_4 з пріорітетом - 2 виконано
запит № client-3_req_5 з пріорітетом - 2 виконано
запит № client-3_req_2 з пріорітетом - 3 виконано
------------- стек - черг (з пріорітетом від 1 до 3) -------------
client-1 виконається першим, так як в стеку інших клієнтів немає. Потім від 4-го до 2-го клієнта
запит № client-1_req_1 з пріорітетом - 2 від client-1 створено
запит № client-1_req_2 з пріорітетом - 3 від client-1 створено
запит № client-1_req_3 з пріорітетом - 2 від client-1 створено
запит № client-1_req_4 з пріорітетом - 1 від client-1 створено
запит № client-2_req_1 з пріорітетом - 1 від client-2 створено
запит № client-3_req_1 з пріорітетом - 2 від client-3 створено
запит № client-3_req_2 з пріорітетом - 1 від client-3 створено
запит № client-3_req_3 з пріорітетом - 2 від client-3 створено
запит № client-3_req_4 з пріорітетом - 3 від client-3 створено
запит № client-2_req_2 з пріорітетом - 2 від client-2 створено
запит № client-2_req_3 з пріорітетом - 1 від client-2 створено
запит № client-2_req_4 з пріорітетом - 3 від client-2 створено
запит № client-2_req_5 з пріорітетом - 3 від client-2 створено
запит № client-1_req_5 з пріорітетом - 1 від client-1 створено
запит № client-4_req_1 з пріорітетом - 2 від client-4 створено
запит № client-4_req_2 з пріорітетом - 2 від client-4 створено
запит № client-4_req_3 з пріорітетом - 3 від client-4 створено
запит № client-4_req_4 з пріорітетом - 1 від client-4 створено
запит № client-4_req_5 з пріорітетом - 2 від client-4 створено
запит № client-1_req_1 з пріорітетом - 2 виконано
запит № client-1_req_4 з пріорітетом - 1 виконано
запит № client-1_req_5 з пріорітетом - 1 виконано
запит № client-1_req_3 з пріорітетом - 2 виконано
запит № client-1_req_2 з пріорітетом - 3 виконано
запит № client-4_req_4 з пріорітетом - 1 виконано
запит № client-4_req_1 з пріорітетом - 2 виконано
запит № client-4_req_2 з пріорітетом - 2 виконано
запит № client-4_req_5 з пріорітетом - 2 виконано
запит № client-4_req_3 з пріорітетом - 3 виконано
запит № client-3_req_2 з пріорітетом - 1 виконано
запит № client-3_req_1 з пріорітетом - 2 виконано
запит № client-3_req_3 з пріорітетом - 2 виконано
запит № client-3_req_4 з пріорітетом - 3 виконано
запит № client-2_req_1 з пріорітетом - 1 виконано
запит № client-2_req_3 з пріорітетом - 1 виконано
запит № client-2_req_2 з пріорітетом - 2 виконано
запит № client-2_req_4 з пріорітетом - 3 виконано
запит № client-2_req_5 з пріорітетом - 3 виконано
завершено виконання всіх запитів від клієнтів
---------------------------  пошук маршруту ---------------------------
a -> b, weight: {'duration': 7, 'distance': 9}
a -> c, weight: {'duration': 9, 'distance': 11}
a -> f, weight: {'duration': 14, 'distance': 10}
b -> a, weight: {'duration': 7, 'distance': 9}
b -> c, weight: {'duration': 10, 'distance': 4}
b -> d, weight: {'duration': 15, 'distance': 8}
c -> a, weight: {'duration': 9, 'distance': 11}
c -> b, weight: {'duration': 10, 'distance': 4}
c -> d, weight: {'duration': 11, 'distance': 3}
c -> f, weight: {'duration': 2, 'distance': 4}
d -> b, weight: {'duration': 15, 'distance': 8}
d -> c, weight: {'duration': 11, 'distance': 3}
d -> e, weight: {'duration': 6, 'distance': 2}
e -> d, weight: {'duration': 6, 'distance': 2}
e -> f, weight: {'duration': 9, 'distance': 4}
f -> a, weight: {'duration': 14, 'distance': 10}
f -> c, weight: {'duration': 2, 'distance': 4}
f -> e, weight: {'duration': 9, 'distance': 4}
Пошук маршруту з використанням рекурсії:
{'route': {'a': 0, 'c': 29, 'f': 8, 'e': 22}, 'weight': 59}
Пошук маршруту з використанням черги:
{'route': ['a', 'c', 'f', 'e'], 'weight': 59}

'''