
'''
Here should come the fitness evaluation functions.
'''

import gaproject.shared
import array

def evalTSP(individual):
    'The most basic evaluation, from the DEAP TSP example:'
    distance_map = gaproject.shared.distance_map

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
    if evaluation == (0.0,):
        print  individual
        raw_input()
    return evaluation


def checkIfValidAdjacent(individual):
    visitedNodes = []
    #always start the representation of the tour with node 0
    currentNode = 0
    for x in individual:
        #if a currentNode has already been visited we have a non valid adjacent individual
        if currentNode in visitedNodes:
            return False
        visitedNodes.append(individual[currentNode])
        currentNode = individual[currentNode]
    return True


def fromAdjacentToPath(individual):
    newIndividual = []
    #always start the representation of the tour with node 0
    currentNode = 0
    newIndividual.append(0)
    while(len(newIndividual) != len(individual)):
        #for each position in individual take the corresponding node
        newIndividual.append(individual[currentNode])
        currentNode = individual[currentNode]
    return array.array('i', newIndividual)


def fromPathToAdjacent(individual):
    newIndividual = array.array('i', [0] * len(individual))
    #for each node look at the adjacent node in the path representation
    for x in range(len(individual)):
        #visit the path representation saving the adjacent node in the new individuak
        newIndividual[individual[x]] = individual[(x + 1) % len(individual)]
    return newIndividual

