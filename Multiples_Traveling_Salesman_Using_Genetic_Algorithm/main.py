import random
import math
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl
from tqdm import tqdm
import time as t

n_cities = 31
n_salesman = 3 #numero de caixeiros
max_cities_per_salesman = 11 #maximo de caixeiros
population_size = 100
generations = 100
mutation_rate = 0.5

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

def total_distance(tours, distances):
    distance = 0
    for tour in tours:
        for i in range(len(tour) - 1):
            distance += distances[tour[i]][tour[i+1]]
        distance += distances[tour[-1]][tour[0]]
    return distance
    
def initial_population(population_size, n_cities, m_salesmen, max_cities_per_salesman): #cria uma populacao inicial onde as cidades sao distribuidas entre os caixeiros
    population = []
    for _ in range(population_size):
        cities = list(range(1, n_cities))
        random.shuffle(cities)
        tours = [[] for _ in range(m_salesmen)]
        for i in range(m_salesmen):
            tours[i].append(0)
        
        i = 0
        while cities:
            if len(tours[i % m_salesmen]) < max_cities_per_salesman + 1:
                tours[i % m_salesmen].append(cities.pop())
            i += 1
        population.append(tours)
    return population

def selection(population, distances):
    ranked_population = sorted(population, key=lambda x: total_distance(x, distances))
    return ranked_population[:max(len(population)//2, 1)]

def crossover(parent1, parent2):
    child = [[] for _ in range(n_salesman)]
    for i in range(n_salesman):
        cities_union = set(parent1[i] + parent2[i])
        cut_point = random.randint(1, len(cities_union))
        child[i] = parent1[i][:cut_point]
        for city in parent2[i]:
            if city not in child[i]:
                child[i].append(city)
        #se o child não tem todas as cidades, add as faltantes do primeiro pai
        for city in parent1[i]:
            if city not in child[i]:
                child[i].append(city)
    return child


def mutate(tours, mutation_rate):
    for tour in tours:
        if random.random() < mutation_rate:
            i, j = random.sample(range(1, len(tour)), 2)
            if j != i:
                tour[i], tour[j] = tour[j], tour[i]
                break
    return tours
def local_search(tours, distances):
    for tour in tours:
        best_distance = total_distance([tour], distances)
        best_tour = tour.copy()
        for i in range(1, len(tour)):
            for j in range(i + 1, len(tour)):
                new_tour = tour[:]
                new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
                new_distance = total_distance([new_tour], distances)
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_tour = new_tour
        # Adicionando a cidade inicial ao final do percurso
        best_tour.append(best_tour[0])
        tour[:] = best_tour
    return tours

def genetic_algorithm(coordinates, population_size, generations, mutation_rate):
    start = t.time()
    distances = create_problem(coordinates)
    for _ in tqdm(range(generations)):
        population = initial_population(population_size, n_cities, n_salesman, max_cities_per_salesman)
    
    for _ in range(generations):
        population = selection(population, distances)
        next_generation = []
        while len(next_generation) < population_size:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            child = local_search(child, distances)
            next_generation.append(child)
        population = next_generation

    end = t.time()
    time = end - start
    best_solution = min(population, key=lambda x: total_distance(x, distances))
    return best_solution, start

def generate_grafico():
    tempos = []
    for i in range(10):
        best_known_solution, delta_tempo = genetic_algorithm(coordinates, population_size, generations, mutation_rate)
        tempos.append(delta_tempo)
    
    prob = [(i - 0.5)/100 for i in range(1,101)]

    tempos.sort()

    ax = pl.subplots()
    ax.autoscale()  # ajusta a figura para fazer caber o desenho
    ax.margins(0.1)
    pl.scatter(tempos, prob)
    pl.title("Gráfico Time-To-Target (TTT) para Simulated Annealing")
    pl.xlabel("Tempo até o Target (s)")
    pl.ylabel("Proporção Acumulada de Execuções (%)")
    pl.show()

distances = create_problem(coordinates)
best_solution = genetic_algorithm(coordinates, population_size, generations, mutation_rate)
print("Best solution:", best_solution)
print("Total distance:", total_distance(best_solution, create_problem(coordinates)))
generate_grafico()