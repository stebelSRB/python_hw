import queue

class VertexParam:

    '''Клас для зберігання параметрів вершин графа
    Параметри: duration, distance'''
    
    param_name = ['duration', 'distance']

    def __init__(self, data: dict):
        self.param = {}
        for key in self.param_name:
            self.param[key] = data.get(key)

    def __iter__(self):
        return iter(self.param.values())

    def __repr__(self):
        return str(self.param)

class Vertex:

    '''Клас для зберігання вершин графа
    Зберігає ідентифікатор вершини та сусідні вершини з параметрами'''

    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, param: VertexParam):
        self.adjacent[neighbor] = param

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_params(self, neighbor):
        return self.adjacent[neighbor]
    
    def edit_param(self, neighbor, key, value):
        if key in VertexParam.param_name:
            self.adjacent[neighbor].param[key] = value
        else:
            raise KeyError(f"Параметр '{key}' некоректний. Дозволені параметри: {VertexParam.param_name}")

class Graph:

    '''Клас для зберігання графа
    Зберігає словник вершин, кількість вершин та параметри маршруту'''

    def __init__(self):
        self.vert_dict = {}
        self.priorites_param_route = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, duration = 0, distance = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        param = VertexParam({'duration': duration, 'distance': distance})
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], param)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], param)

    def get_vertices(self):
        return self.vert_dict.keys()
    
    def set_priorites_param_to_route(self, param_name: str, weight: int = 1):        
        self.priorites_param_route[param_name] = weight

    def calculate_weight(self, frm, to):

        '''Обчислює вагу маршруту між двома вершинами на основі параметрів'''

        total_weight = 0
        params =  self.vert_dict[frm].get_params(self.vert_dict[to]).param
        for key, value in params.items():
            if key in self.priorites_param_route:
                total_weight += value * self.priorites_param_route[key]
            else:
                total_weight += value
        return total_weight
    
    def search_route_recursion(self, start, end, route = None, weight = 0):

        '''Рекурсивний пошук маршруту між двома вершинами
        Повертає словник з маршрутом та вагою маршруту'''

        # print(f"Пошук маршруту з {start} до {end}")        
        if route is None:
            route = {}
        route[start] = weight
        best_route = None

        if start == end: # кінець маршруту
            # print(f"{start} Кінцевий маршрут: {route} з вагою {weight}")
            route_weight = sum(route.values())
            return {'route': route, 'weight': route_weight}

        for next_vertex in self.vert_dict[start].get_connections():
            vertex_id = next_vertex.get_id()
            if vertex_id in route: # циклічний маршрут
                # print(f"{start} Циклічний маршрут:: to {vertex_id} curr {route}")
                continue            
            else: # продовження пошуку маршруту
                # print(f"{start} Продовження пошуку маршруту: to {vertex_id} currr {route}")
                weight_current = self.calculate_weight(start, vertex_id) 
                result = self.search_route_recursion(vertex_id, end, route.copy(), weight_current)
                if best_route is None or (result and result['weight'] < best_route['weight']):
                    best_route = result

        return best_route
    
    def search_route_queue(self, start, end):

        '''Пошук маршруту між двома вершинами з використанням черги
        Повертає словник з маршрутом та вагою маршруту'''

        route_queue = queue.PriorityQueue()
        path_route = [start]
        route_queue.put((0, (start, path_route)))
        visited = set()

        while not route_queue.empty():
            route_weight, route_curr = route_queue.get()
            current_vertex, path_route = route_curr
            # print(f"Поточний маршрут: {path_route} з вагою {route_weight} від {current_vertex}")

            if current_vertex == end:
                return {'route': path_route, 'weight': route_weight}

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            for next_vertex in self.vert_dict[current_vertex].get_connections():
                vertex_id = next_vertex.get_id()
                if vertex_id not in path_route:
                    current_weight = self.calculate_weight(current_vertex, vertex_id) 
                    new_route_weight = route_weight + current_weight
                    new_path_route = path_route.copy()
                    new_path_route.append(vertex_id)
                    # print(f"Додаємо до маршруту: {new_path_route} з вагою {new_route_weight} від {current_vertex} до {vertex_id}")
                    route_queue.put((new_route_weight, (vertex_id, new_path_route)))
        
