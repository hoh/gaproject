
'''
Here should come the fitness evaluation functions.
'''

import gaproject.shared


def evalTSP(individual):
    'The most basic evaluation, from the DEAP TSP example:'
    distance_map = gaproject.shared.distance_map

    distance = distance_map[individual[-1]][individual[0]]
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += distance_map[gene1][gene2]
    return distance,
