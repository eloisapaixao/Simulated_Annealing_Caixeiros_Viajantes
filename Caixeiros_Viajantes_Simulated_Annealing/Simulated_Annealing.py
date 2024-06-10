import random
import math
import copy
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl

n_cities = 92 #número de cidades
n_salesman = 5

coordinates = [
    (500, 500), (354, 968), (582, 631), (411, 807), (153, 112), (505, 398),
    (117, 730), (854, 568), (234, 931), (140, 725), (499, 319), (632, 956),
    (220, 520), (86, 12), (689, 560), (580, 845), (984, 339), (653, 282),
    (615, 278), (840, 501), (967, 289), (804, 22), (795, 741), (263, 847),
    (601, 850), (150, 800), (390, 969), (967, 117), (279, 909), (711, 399),
    (435, 707), (949, 661), (590, 776), (616, 836), (414, 335), (779, 251),
    (34, 986), (567, 90), (420, 780), (811, 535), (868, 563), (487, 937),
    (991, 195), (938, 91), (666, 333), (243, 527), (247, 770), (257, 731),
    (159, 596), (23, 1), (225, 558), (112, 306), (965, 492), (655, 810),
    (545, 178), (467, 143), (704, 298), (902, 210), (111, 303), (842, 978),
    (252, 286), (481, 122), (42, 875), (868, 379), (624, 785), (19, 213),
    (737, 684), (854, 931), (906, 247), (726, 15), (905, 787), (968, 995),
    (293, 355), (592, 311), (94, 584), (337, 619), (902, 561), (82, 710),
    (766, 539), (602, 185), (975, 768), (727, 782), (136, 946), (567, 892),
    (616, 98), (536, 730), (311, 585), (164, 43), (713, 690), (445, 631),
    (840, 935), (257, 761)
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
best_known_solution = annealing(initial_solution=initial_sol, n_maximum_iterations=50000, verbose=True)

print("Best known solution:", best_known_solution)
print("Total distance:", get_total_distance(best_known_solution))

plot_tour(coordinates, best_known_solution)