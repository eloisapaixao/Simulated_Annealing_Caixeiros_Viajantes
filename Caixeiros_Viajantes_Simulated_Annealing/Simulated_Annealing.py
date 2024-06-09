import random
import math
import sys 
import copy
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl

n_cities = 17 #número de cidades
n_salesman = 6

distances = [
    [   0,  548,  776,  696,  582,  274,  502,  194,  308,  194,  536,  502,  388,  354,  468,  776,  662],
    [ 548,    0,  684,  308,  194,  502,  730,  354,  696,  742, 1084,  594,  480,  674, 1016,  868, 1210],
    [ 776,  684,    0,  992,  878,  502,  274,  810,  468,  742,  400, 1278, 1164, 1130,  788, 1552,  754],
    [ 696,  308,  992,    0,  114,  650,  878,  502,  844,  890, 1232,  514,  628,  822, 1164, 560,  1358],
    [ 582,  194,  878,  114,    0,  536,  764,  388,  730,  776, 1118,  400,  514,  708, 1050,  674, 1244],
    [ 274,  502,  502,  650,  536,    0,  228,  308,  194,  240,  582,  776,  662,  628,  514, 1050,  708],
    [ 502,  730,  274,  878,  764,  228,    0,  536,  194,  468,  354, 1004,  890,  856,  514, 1278,  480],
    [ 194,  354,  810,  502,  388,  308,  536,    0,  342,  388,  730,  468,  354,  320,  662,  742,  856],
    [ 308,  696,  468,  844,  730,  194,  194,  342,    0,  274,  388,  810,  696,  662,  320, 1084,  514],
    [ 194,  742,  742,  890,  776,  240,  468,  388,  274,    0,  342,  536,  422,  388,  274,  810,  468],
    [ 536, 1084,  400, 1232, 1118,  582,  354,  730,  388,  342,    0,  878,  764,  730,  388, 1152,  354],
    [ 502,  594, 1278,  514,  400,  776, 1004,  468,  810,  536,  878,    0,  114,  308,  650,  274,  844],
    [ 388,  480, 1164,  628,  514,  662,  890,  354,  696,  422,  764,  114,    0,  194,  536,  388,  730],
    [ 354,  674, 1130,  822,  708,  628,  856,  320,  662,  388,  730,  308,  194,    0,  342,  422,  536],
    [ 468, 1016,  788, 1164, 1050,  514,  514,  662,  320,  274,  388,  650,  536,  342,    0,  764,  194],
    [ 776,  868, 1552,  560,  674, 1050, 1278,  742, 1084,  810, 1152,  274,  388,  422,  764,    0,  798],
    [ 662, 1210,  754, 1358, 1244,  708,  480,  856,  514,  468,  354,  844,  730,  536,  194,  798,    0],
]

def get_total_distance(tour : list) -> int:

    total_distance = 0

    for i in range(n_cities - 1):

        total_distance = total_distance + distances[tour[i]][tour[i + 1]]

    total_distance = total_distance + distances[tour[-1]][tour[0]]

    return total_distance


# swap cities at positions i and j with each other
def swap(tours):
    # Seleciona dois vendedores diferentes aleatoriamente
    salesman_a = random.randint(0, len(tours) - 1)
    salesman_b = random.randint(0, len(tours) - 1)
    
    while salesman_a == salesman_b:  # Garante que sejam diferentes
        salesman_b = random.randint(0, len(tours) - 1)
    
    # Seleciona uma cidade de cada vendedor
    if tours[salesman_a] and tours[salesman_b]:  # Verifica que ambos os vendedores têm cidades
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

def generate_lines(coordinates, tour):
    lines = []
    colors = []

    # Gerar uma cor aleatória para cada linha
    for _ in range(len(tour) - 1):
        colors.append((random.random(), random.random(), random.random()))

    for j in range(len(tour) - 1):
        lines.append([
            coordinates[tour[j]],
            coordinates[tour[j+1]]
        ])

    lines.append([
        coordinates[tour[-1]],
        coordinates[tour[0]] # vai do ultimo ao primeiro
    ])

    return lines, colors

def plot_tour(coordinates, tour):
    lines, colors = generate_lines(coordinates, tour)
    lc = mc.LineCollection(lines, colors=colors, linewidths=2)  # Adicionando as cores
    # subplot == uma folha em branco para desenharmos 
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale() # ajusta a figura para fazer caber o desenho
    ax.margins(0.1)
    # scatter == grafo
    pl.scatter([i[0] for i in coordinates], [i[1] for i in coordinates])
    pl.title("Tour")
    pl.xlabel("X")
    pl.ylabel("Y")
    pl.show()

best_known_solution = annealing(initial_solution = random.sample(range(n_cities), n_cities), n_maximum_iterations = 3000, verbose = True)

print(best_known_solution, get_total_distance(best_known_solution))