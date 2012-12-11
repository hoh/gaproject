
from deap import creator
import random
import shared




def cxSCX(individual1, individual2):
    """
    Function that creates an instance of CXSCXCalculator and performs the crossover

    """
    return CXSCXCalculator(individual1, individual2, distanceMap).crossover()

class CXSCXCalculator:
    """
    Contains the logic to perform sequential constructive crossover
    see: http://www.cscjournals.org/csc/manuscript/Journals/IJBB/volume3/Issue6/IJBB-41.pdf

    """
    def __init__(self, individual1, individual2):
        self.individual2 = individual2
        self.individual1 = individual1
        self.visitedNodes = []
        self.sequent

    def crossover(self):
        child = creator.Individual()
        #start at one
        currentNodePosIn1 = self.individual1.index(1)
        currentNodePosIn2 = self.individual2.index(1)
        self.visitedNodes.append(1)

        while(True):
            candidateLegitNodeIn1 = self.individual1[(currentNodePosIn1 + 1) % len(individual1)]
            candidateLegitNodeIn2 = self.individual2[(currentNodePosIn2 + 1) % len(individual2)]
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
                if shared.distanceMap[currentNodePosIn1][candidateLegitNodeIn1] > shared.distanceMap[currentNodePosIn2][candidateLegitNodeIn2]:
                    child.append(self.individual2[currentNodePosIn2])
                else
                    child.append(self.individual1[currentNodePosIn1])
            else:
                child.append(_getSequentialNode())

        return child

    def _geteSequentialNode(self):
        return 1


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
