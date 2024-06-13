import random
import math
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl
from tqdm import tqdm
import time as t

n_cities = 139
n_salesman = 7 #numero de caixeiros
max_cities_per_salesman = 20 #maximo de caixeiros
population_size = 100
generations = 100
mutation_rate = 0.5

coordinates = [
(500, 500), (176, 308), (908, 557), (846, 73), (26, 911), (670, 606),
(35, 365), (62, 327), (746, 763), (476, 692), (511, 552), (457, 357),
(104, 543), (583, 243), (327, 986), (112, 375), (157, 976), (592, 150),
(836, 306), (360, 586), (218, 411), (355, 731), (45, 876), (991, 476),
(582, 148), (118, 293), (965, 175), (713, 185), (782, 914), (532, 820),
(784, 173), (936, 797), (822, 984), (710, 661), (88, 759), (607, 151),
(16, 155), (915, 189), (96, 851), (710, 921), (641, 585), (327, 874),
(675, 805), (117, 88), (646, 692), (709, 315), (17, 990), (556, 947),
(788, 415), (997, 575), (713, 922), (693, 619), (12, 208), (955, 194),
(635, 603), (116, 104), (777, 813), (613, 64), (60, 225), (828, 27),
(564, 358), (172, 954), (45, 346), (21, 123), (292, 982), (930, 973),
(185, 251), (94, 842), (689, 634), (108, 484), (700, 827), (207, 912),
(221, 117), (202, 861), (665, 504), (77, 293), (459, 894), (756, 791),
(512, 492), (671, 666), (856, 985), (701, 278), (540, 622), (48, 871),
(894, 970), (206, 569), (278, 591), (309, 418), (760, 67), (292, 309),
(236, 440), (503, 84), (864, 198), (304, 152), (782, 503), (910, 351),
(620, 360), (442, 273), (442, 669), (619, 763), (207, 247), (508, 934),
(984, 828), (833, 425), (928, 854), (250, 528), (27, 33), (641, 433),
(311, 83), (70, 971), (910, 799), (244, 312), (483, 515), (502, 262),
(39, 114), (884, 556), (201, 612), (939, 247), (635, 265), (978, 165),
(421, 782), (882, 615), (421, 885), (847, 996), (617, 584), (403, 248),
(142, 118), (331, 146), (2, 683), (451, 283), (313, 854), (796, 5),
(463, 162), (881, 196), (544, 391), (644, 755), (573, 910), (848, 820),
(437, 614), (868, 985)
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