import threading
import queue
import time
import random

queue_server = None

def worker_front_end(queue_client, client_name):

    '''
        Функція, яка створює запити від клієнта і додає їх до черги серверу
        queue_client - черга клієнта, в яку будуть додаватися запити
        client_name - ім'я клієнта, для якого створюються запити
    '''
    
    count_requests = random.randint(3, 5)

    for i in range(count_requests):
        request = f"{client_name}_req_{i+1}"
        priority = random.randint(1, 3)
        queue_client.put((priority, request))
        print(f"запит № {request} з пріорітетом - {priority} від {client_name} створено")

def worker_back_end():

    '''
        Функція, яка обробляє запити від клієнтів
        queue_server - загальна черга серверу, в яку будуть додаватися черги клієнтів
    '''

    print(f"{threading.current_thread().name} старт")
    while True:
        if not queue_server.empty():
            queue_client = queue_server.get()
            task_run = True
            while task_run or not queue_client.empty():
                if queue_client.empty():
                    continue
                else:
                    task_run = False
                priority, request = queue_client.get()
                time.sleep(random.uniform(0.5, 0.9))
                queue_client.task_done()
                print(f"запит № {request} з пріорітетом - {priority} виконано")
            queue_server.task_done()  

def demo_client_server():

    '''
        Функція, яка демонструє роботу клієнт-серверної архітектури
        Створює загальну чергу серверу та черги клієнтів, запускає потоки для обробки запитів
    '''

    print('------------- черга - черг (з пріорітетом від 1 до 3 та maxsize=2) -------------')
    # створюємо загальну чергу серверу
    global queue_server
    queue_server = queue.Queue()
    threading.Thread(target=worker_back_end, name=f'worker_back_end', daemon=True).start()

    # імітуємо паралельні запити від клієнтів
    for i in range(3):    
        client_name = f'client-{i+1}'
        queue_client = queue.PriorityQueue(maxsize=2)  
        queue_server.put(queue_client)
        threading.Thread(target=worker_front_end, args=(queue_client, client_name), name=f'worker_front_end-{i+1}').start()

    # Чекаємо виконання запитів від клієнтів
    queue_server.join()

    print('------------- стек - черг (з пріорітетом від 1 до 3) -------------')
    print('client-1 виконається першим, так як в стеку інших клієнтів немає. Потім від 4-го до 2-го клієнта')

    queue_server =  queue.LifoQueue() 

    for i in range(4):    
        client_name = f'client-{i+1}'
        queue_client = queue.PriorityQueue()  
        queue_server.put(queue_client)
        threading.Thread(target=worker_front_end, args=(queue_client, client_name), name=f'worker_front_end-{i+1}').start()

    # Чекаємо виконання запитів від клієнтів
    queue_server.join()
    print('завершено виконання всіх запитів від клієнтів')


