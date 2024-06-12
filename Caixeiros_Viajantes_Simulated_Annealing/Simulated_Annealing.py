import random
import math
import copy
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl

n_cities = 47 #número de cidades
n_salesman = 3

coordinates = [
    (500, 500), (513, 714), (570, 348), (93, 807), (52, 705), (35, 319),
    (80, 797), (167, 395), (812, 120), (37, 583), (672, 272), (716, 356),
    (769, 932), (660, 402), (304, 161), (829, 649), (451, 593), (92, 217),
    (418, 290), (532, 496), (397, 443), (564, 994), (228, 718), (587, 846),
    (992, 762), (529, 824), (373, 865), (108, 982), (452, 167), (963, 181),
    (584, 544), (477, 954), (426, 643), (205, 947), (230, 764), (294, 88),
    (27, 932), (827, 933), (569, 980), (871, 618), (469, 326), (492, 826),
    (487, 172), (682, 860), (45, 97), (582, 614), (491, 971), (327, 871)
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

    return best_known_solution

def generate_lines(coordinates, tours):
    lines = []
    colors = []

    # Gera uma cor aleatória para cada vendedor
    for i in range(len(tours)):
        color = (random.random(), random.random(), random.random())
        tour = tours[i]
        for j in range(len(tour) - 1):
            lines.append([
                coordinates[tour[j]],
                coordinates[tour[j + 1]]
            ])
            colors.append(color)
        lines.append([
            coordinates[tour[-1]],
            coordinates[tour[0]]  # vai do ultimo ao primeiro
        ])
        colors.append(color)

    return lines, colors

def plot_tour(coordinates, tours):
    lines, colors = generate_lines(coordinates, tours)
    lc = mc.LineCollection(lines, colors=colors, linewidths=2)  # Adicionando as cores
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()  # ajusta a figura para fazer caber o desenho
    ax.margins(0.1)
    pl.scatter([i[0] for i in coordinates], [i[1] for i in coordinates])
    pl.title("Tour")
    pl.xlabel("X")
    pl.ylabel("Y")
    pl.show()

distances = create_problem(coordinates)
initial_sol = initial_solution(n_cities, n_salesman)
best_known_solution = annealing(initial_solution=initial_sol, n_maximum_iterations=8000, verbose=True)

print("Best known solution:", best_known_solution)
print("Total distance:", get_total_distance(best_known_solution))

plot_tour(coordinates, best_known_solution)