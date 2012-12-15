
'''
Here should come the fitness evaluation functions.
'''

import gaproject.shared
from gaproject.tools.adjacent import checkIfValidAdjacent, fromAdjacentToPath


def evalTSP(individual):
    'The most basic evaluation, from the DEAP TSP example:'
    distance_map = gaproject.shared.data.dist_matrix()

    distance = distance_map[individual[-1]][individual[0]]
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += distance_map[gene1][gene2]
    return distance,


def evalTSPAdjacentEdges(individual):
    #if individual is not a valid adjacent representation then it is a path representation
    #we change once that individual to path representation
    if not checkIfValidAdjacent(individual):
        raise ValueError("Individual is not valid according to adjacent representation.\n", individual)
    evaluation = evalTSP(fromAdjacentToPath(individual))
    return evaluation

__all__ = evalTSP, evalTSPAdjacentEdges
