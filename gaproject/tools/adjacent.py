
import array


def checkIfValidAdjacent(individual):
    visitedNodes = []
    #always start the representation of the tour with node 0
    currentNode = 0
    while(len(visitedNodes) != len(individual)):
        #if a currentNode has already been visited we have a non valid adjacent individual
        if currentNode in visitedNodes:
            return False
        visitedNodes.append(currentNode)
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

    return newIndividual


def fromPathToAdjacent(individual):
    newIndividual = array.array('i', [0] * len(individual))
    #for each node look at the adjacent node in the path representation
    for x in range(len(individual)):
        #visit the path representation saving the adjacent node in the new individuak
        newIndividual[individual[x]] = individual[(x + 1) % len(individual)]
    return newIndividual
