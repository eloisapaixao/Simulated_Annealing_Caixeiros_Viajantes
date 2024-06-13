import random
import math
import copy
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl
import time

n_cities = 31 #número de cidades
n_salesman = 3

coordinates = [
(500, 500), (826, 465), (359, 783), (563, 182), (547, 438), (569, 676),
(989, 416), (648, 750), (694, 978), (493, 969), (175, 89), (104, 130),
(257, 848), (791, 249), (952, 204), (34, 654), (89, 503), (548, 964),
(492, 34), (749, 592), (536, 875), (373, 708), (385, 260), (560, 751),
(304, 516), (741, 368), (59, 131), (154, 681), (425, 456), (885, 783),
(30, 415), (61, 25)
]

def create_problem(coordinates):
    n_cities = len(coordinates)

    distances = [[0 for _ in range(n_cities)] for _ in range(n_cities)]

    for i in range(n_cities):
        for j in range(i + 1, n_cities):
            x = coordinates[i][0] - coordinates[j][0]
            y = coordinates[i][1] - coordinates[j][1]
            distance = math.sqrt(x**2 + y**2) 
            distances[i][j] = distances[j][i] = distance
        
    return distances

#Calcula a distância total percorrida por todos os caixeiros-viajantes
def get_total_distance(tours):
    total_distance = 0
    for tour in tours:
        for i in range(len(tour) - 1):
            total_distance += distances[tour[i]][tour[i + 1]]
        if tour:
            total_distance += distances[tour[-1]][tour[0]]
    return total_distance

#Calcula a solução inicial aleatória
def initial_solution(n_cities, n_salesman):
    cities = list(range(n_cities))
    random.shuffle(cities)
    return [cities[i::n_salesman] for i in range(n_salesman)]

# swap cities at positions i and j with each other
def swap(tours):
    # Seleciona dois vendedores diferentes aleatoriamente
    salesman_a = random.randint(0, len(tours) - 1)
    salesman_b = random.randint(0, len(tours) - 1)
    
    while salesman_a == salesman_b or not tours[salesman_a] or not tours[salesman_b]:  # Garante que sejam diferentes
        salesman_b = random.randint(0, len(tours) - 1)
    
    # Seleciona uma cidade de cada vendedor
    city_a = random.randint(0, len(tours[salesman_a]) - 1)
    city_b = random.randint(0, len(tours[salesman_b]) - 1)
        
    # Troca as cidades entre os vendedores
    tours[salesman_a][city_a], tours[salesman_b][city_b] = tours[salesman_b][city_b], tours[salesman_a][city_a]
    
    return tours

# returns neighbor of your solution.
def get_neighbors(current_solution):
    return swap(current_solution)

def annealing(initial_solution, n_maximum_iterations, verbose = False):

    inicio = time.time()

    current_temperature = 100

    alpha = (1 / current_temperature)**(1.00 / n_maximum_iterations)

    current_solution = initial_solution

    best_known_solution = initial_solution

    for k in range(n_maximum_iterations):

        neighbor_solution = get_neighbors(copy.deepcopy(current_solution))

        delta = get_total_distance(current_solution) - get_total_distance(neighbor_solution)

        if delta > 0 or random.uniform(0, 1) < math.exp(float(delta) / float(current_temperature)):
            current_solution = neighbor_solution

        if get_total_distance(current_solution) < get_total_distance(best_known_solution):
            best_known_solution = current_solution

            if verbose:
                print(k, current_temperature, get_total_distance(best_known_solution))
        
        current_temperature = alpha * current_temperature
    
    fim = time.time()

    tempo = fim - inicio

    return best_known_solution, tempo

def generate_grafico():
    tempos = []
    for i in range(100):
        best_known_solution, delta_tempo = annealing(initial_solution=initial_sol, n_maximum_iterations=8000, verbose=True)
        tempos.append(delta_tempo)
    
    prob = [(i - 0.5)/100 for i in range(1,101)]

    tempos.sort()

    ax = pl.subplots()
    pl.scatter(tempos, prob)
    pl.title("Gráfico Time-To-Target (TTT) para Simulated Annealing")
    pl.xlabel("Tempo até o Target (s)")
    pl.ylabel("Proporção Acumulada de Execuções (%)")
    pl.show()


distances = create_problem(coordinates)
initial_sol = initial_solution(n_cities, n_salesman)
generate_grafico()