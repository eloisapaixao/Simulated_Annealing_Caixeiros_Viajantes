import random
import math
import copy
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl

n_cities = 139 #número de cidades
n_salesman = 7

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