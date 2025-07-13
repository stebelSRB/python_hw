from collections import deque

def create_tower_of_hanoi(n):
    
    source = deque()
    for i in range(n, 0, -1):
        source.append(i)
    return {'source': source, 'destination': deque(), 'auxiliary': deque()}

def change_tower_of_hanoi(tower_of_hanoi, source, destination):

    element = tower_of_hanoi[source].pop()
    tower_of_hanoi[destination].append(element)
    print(tower_of_hanoi)
    return tower_of_hanoi

def run_calculation(n):
        
    tower_of_hanoi = create_tower_of_hanoi(n)
    print('Initial state of Tower of Hanoi:')
    print(tower_of_hanoi)
    print(f'Starting Tower of Hanoi with {n} disks...')
    tower_of_hanoi = TowerOfHanoi(n, tower_of_hanoi, 'source', 'destination', 'auxiliary')
    print('Final state of Tower of Hanoi:')
    print(tower_of_hanoi)

def TowerOfHanoi(n, tower_of_hanoi, source, destination, auxiliary,):

    if n==1:
        tower_of_hanoi = change_tower_of_hanoi(tower_of_hanoi, source, destination)
        return tower_of_hanoi
    
    tower_of_hanoi = TowerOfHanoi(n-1, tower_of_hanoi, source, auxiliary, destination)  
    tower_of_hanoi = change_tower_of_hanoi(tower_of_hanoi, source, destination)
    tower_of_hanoi = TowerOfHanoi(n-1, tower_of_hanoi, auxiliary, destination, source)

    return tower_of_hanoi
