# --------------------------- Homework_9  ------------------------------------
r'''

Виконав: Роман Стебельський
Homework_9
    Завдання_1.
    Скрипт файлу hw_9_1_fibonachchi.py реалізує рекурсивний розрахунок чисел ряду
    Фібоначчі. Проведіть рефакторинг (редагування) програмного коду, з отриманням трьох
    рішень:
    1.1. Шляхом створення ітератора – iterator;
    1.2. Шляхом створення генераторної функції – generator function;
    1.3. Шляхом створення генераторного виразу – generator expression.
    Рішення представити як окремі модулі.
    *** Послідовність чисел Фібоначчі має вираз Fn = Fn-1 + Fn-2: наступне число є
    сумою двох попередніх.

    Завдання_2.
    Скрипт файлу hw_9_2_rand_norm.py реалізує формування нормального закону
    розподілу випадкової величини, як адитивна суміш двох рівномірних законів за
    принципами циклічних повторень. Проведіть рефакторинг (редагування) програмного
    коду, з отриманням трьох рішень:
    1.1. Шляхом створення ітератора – iterator;
    1.2. Шляхом створення генераторної функції – generator function;
    1.3. Шляхом створення генераторного виразу – generator expression.
    Рішення представити як окремі модулі із створення Virtual Environment, та
    requirements.txt

Package            Version
------------------ -----------
matplotlib         3.10.1
numpy              2.2.5
'''

import fibonachchi as f
import rand_norm as rn
import matplotlib.pyplot as plt

# ---------------------------------- головні виклики --------------------------------
if __name__ == "__main__":

    print('---------- Числа ряду Фібоначчі ----------')
    print('Демонстрація розрахунок чисел ряду Фібоначчі – generator function')
    for i in f.FibGenerator(7):
        print(i)

    print('Демонстрація розрахунок чисел ряду Фібоначчі – generator expression')
    for i in f.FibExpression(3):
        print(i)

    print('Демонстрація розрахунок чисел ряду Фібоначчі – iterator')
    fib_iterator = f.FibIterator(3)
    for i in fib_iterator:
        print(i)

    try:
        print(next(fib_iterator))
    except StopIteration:
        print('Розрахунок ряду чисел завершено')

    print('---------- Нормального закону розподілу ВВ ----------')
    n = 10000
    print('Демонстрація розрахунок нормального закону розподілу ВВ – generator function')
    v1 = rn.BBgenerator(n)
    v2 = rn.BBgenerator(n)
    normDest_generator = rn.RNgenerator(n, v1, v2)

    print('Демонстрація розрахунок нормального закону розподілу ВВ – generator expression')
    normDest_expression = rn.RNexpression(n)

    print('Демонстрація розрахунок нормального закону розподілу ВВ – iterator')
    v1_for_iterator = rn.BBgenerator(n)
    v2_for_iterator = rn.BBgenerator(n)
    normDest_iterator = rn.RNiterator(n, v1_for_iterator, v2_for_iterator)

    print('Починаємо прохід ітераторів шляхом передачі їх як параметр для list')
    plt.hist(list(normDest_generator), bins=15)
    plt.title("generator function")
    plt.show()
    plt.hist(list(normDest_expression), bins=15)
    plt.title("generator expression")
    plt.show()
    plt.hist(list(normDest_iterator), bins=15)
    plt.title("iterator")
    plt.show()

r'''    
Результат:
---------- Числа ряду Фібоначчі ----------
Демонстрація розрахунок чисел ряду Фібоначчі – generator function
0
1
1
2
3
5
8
13
Демонстрація розрахунок чисел ряду Фібоначчі – generator expression
0
1
1
2
Демонстрація розрахунок чисел ряду Фібоначчі – iterator
0
1
1
2
Розрахунок ряду чисел завершено
---------- Нормального закону розподілу ВВ ----------
Демонстрація розрахунок нормального закону розподілу ВВ – generator function
Демонстрація розрахунок нормального закону розподілу ВВ – generator expression
Демонстрація розрахунок нормального закону розподілу ВВ – iterator
Починаємо прохід ітераторів шляхом передачі їх як параметр для list

Process finished with exit code 0

'''