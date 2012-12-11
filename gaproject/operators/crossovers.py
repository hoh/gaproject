
from deap import creator
import random
import gaproject.shared as shared
import numpy


def cxEnhancedSCX(individual1, individual2):
    """
    Function that creates an instance of CXSCXCalculator and performs the simple SCX crossover

    """
    medians = numpy.median(shared.distance_map, axis=1)
    defaultSequence = range(1, len(individual1))
    sequenceOfNodes = sorted(defaultSequence)
    #creating the sequence of nodes like this is inneficient BUT it should work for the time being.
    return CXSCXCalculator(individual1, individual2, sequenceOfNodes).crossover()


def cxSimpleSCX(individual1, individual2):
    """
    Function that creates an instance of CXSCXCalculator and performs the simple SCX crossover

    """
    sequenceOfNodes = [x for x in range(2, len(individual1))]
    return CXSCXCalculator(individual1, individual2, sequenceOfNodes).crossover()


class CXSCXCalculator:

    """
    Contains the logic to perform sequential constructive crossover
    see: http://www.cscjournals.org/csc/manuscript/Journals/IJBB/volume3/Issue6/IJBB-41.pdf

    """

    def __init__(self, individual1, individual2, sequenceOfNodes):
        self.individual2 = individual2
        self.individual1 = individual1
        self.visitedNodes = []
        self.sequenceOfNodes = sequenceOfNodes

    def crossover(self):
        child = creator.Individual()
        #start with node number 1
        currentNode = 1
        self.visitedNodes.append(1)
        while(True):
            currentNodePosIn1 = self.individual1.index(currentNode)
            currentNodePosIn2 = self.individual2.index(currentNode)
            candidateLegitNodeIn1 = self.individual1[(currentNodePosIn1 + 1) % len(self.individual1)]
            candidateLegitNodeIn2 = self.individual2[(currentNodePosIn2 + 1) % len(self.individual2)]
            #check if the candidate node in individual 1 has not been visited
            if candidateLegitNodeIn1 not in self.visitedNodes:
                legitNodeIn1 = candidateLegitNodeIn1
            else:
                legitNodeIn1 = None
            #check if the candidate node in individual 2 has not been visited 
            if candidateLegitNodeIn2 not in self.visitedNodes:
                legitNodeIn2 = candidateLegitNodeIn2
            else:
                legitNodeIn2 = None
            #if both individuals contain legit nodes, chose the one forming the edge
            #with lowest cost
            if(legitNodeIn1 and legitNodeIn2):
                if shared.distance_map[currentNode][legitNodeIn1] > shared.distance_map[currentNode][legitNodeIn2]:
                    child.append(legitNodeIn2)
                    self.visitedNodes.append(legitNodeIn2)
                    currentNode = legitNodeIn2
                    if len(child) == len(self.individual1):
                        break
                else:
                    child.append(legitNodeIn1)
                    self.visitedNodes.append(legitNodeIn1)
                    currentNode = legitNodeIn1
                    if len(child) == len(self.individual1):
                        break
            else:
                sequentialNode = self._getSequentialNode()
                child.append(sequentialNode)
                self.visitedNodes.append(sequentialNode)
                currentNode = sequentialNode
                if len(child) == len(self.individual1):
                        break

        return child

    def _getSequentialNode(self):
        for node in self.sequenceOfNodes:
            if node not in self.visitedNodes:
                self.visitedNodes.append(node)
                return node


def cxERX(individual1, individual2):
    """
    Function that creates an instance of CXERXCalculator and performs the crossover

    """
    return CXERXCalculator(individual1, individual2).crossover()


class CXERXCalculator:
    """
    Contains the logic to perform the ERX crossover. ERX crossover is based on:
    1. creation of an edgeMap
    2. creation of child based on to the child a random node at first,
    then the less connected nodes

    """

    def __init__(self, individual1, individual2):
        self.individual2 = individual2
        self.individual1 = individual1
        self.edgeMap = {}

    def crossover(self):
        self._buildEdgeMap()
        return self._createChild()

    def _createChild(self):
        child = creator.Individual()
        #step1
        currentNode = self.individual1[random.randint(0, len(self.individual1) - 1)]
        while True:
            child.append(currentNode)
            #extract the nodes linked to current node
            neighborgs = self.edgeMap.pop(currentNode)
            neighborgs = list(neighborgs)
            #remove references to the current node
            self._cleanupNodeFromEdgeMap(currentNode)
            if neighborgs != []:
                #find which neighborg node has the less edges
                currentNeighborg = neighborgs[0]
                currentLen = len(self.edgeMap[currentNeighborg])
                for neighborg in neighborgs:
                    if len(self.edgeMap[neighborg]) < currentLen:
                        currentLen = len(self.edgeMap[neighborg])
                        currentNeighborg = neighborg
                #the neighborg with the less edges is the next node in the child
                currentNode = currentNeighborg
            else:
                if self.edgeMap == {}:
                    break  # if there are no more nodes to assign then stop
                else:
                    #chose as next node any remaining node at random
                    currentNode = self.edgeMap.keys()[random.randint(0, len(self.edgeMap.keys()) - 1)]
        return child

    def _buildEdgeMap(self):
        """
        For each node looks at the corresponding edges in each individual and creates
        an edgeMap entry with as a set of neighboring nodes

        """
        for node in self.individual1:
            pos1 = self.individual1.index(node)
            pos2 = self.individual2.index(node)
            neighborg1 = self.individual1[(pos1 - 1) % len(self.individual1)]
            neighborg2 = self.individual1[(pos1 + 1) % len(self.individual1)]
            neighborg3 = self.individual2[(pos2 - 1) % len(self.individual2)]
            neighborg4 = self.individual2[(pos2 + 1) % len(self.individual2)]
            self.edgeMap[node] = set([neighborg1, neighborg2, neighborg3, neighborg4])

    def _cleanupNodeFromEdgeMap(self, referenceNode):
        """
        Removes any reference to the given node and removes nodes that as a result have no more edges.

        """
        edgeMapEntriesToBeRemoved = []
        for node in self.edgeMap:
            if referenceNode in self.edgeMap[node]:
                self.edgeMap[node].remove(referenceNode)
            if self.edgeMap[node] == set():
                edgeMapEntriesToBeRemoved.append(node)
        for node in edgeMapEntriesToBeRemoved:
                edgeMapEntriesToBeRemoved.remove(node)
