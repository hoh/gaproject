
from deap import creator
import random
import gaproject.shared as shared

# Importing the ordered crossover from DEAP
from deap import tools
cxOrdered = tools.cxOrdered
cxPMX = tools.cxPartialyMatched


def cxNull(individual1, individual2):
    'The awesome Null crossover which does nothing.'
    return individual1, individual2


def cxHeuristic(individual1, individual2):
    child1 = cxHeuristic(individual1,individual2).crossover()
    child2 = cxHeuristic(individual2,individual1).crossover()
    individual1[:] = child1[:]
    individual2[:] = child2[:]
    return individual1, individual2

class cxHeuristic:

    """
    Contains the logic to perform heuristic crossover. Only valid for adjacent representation.

    """

    def __init__(self, individual1, individual2):
        self.individual2 = individual2
        self.individual1 = individual1


    def crossover(self):
        """
        This crossover expects individuals according to adjacent representation.
        It tries to save edges that have lower cost.
        In order to avoid loops, random edges are created (note that this is a sort of mutation)

        """

        child = creator.Individual()
        #temporarily we fill in child using the values in self.individual1
        #these values will be overwritten
        child[:] = self.individual1[:]
        availableNodes = range(len(self.individual1))
        visitedNodes = []
        #chose a node at random to start with
        currentNode = random.randint(0, len(self.individual1) - 1)
        availableNodes.pop(currentNode)
        visitedNodes.append(currentNode)
        while(len(child) != len(self.individual1)):
            #copmare which edge is shorter in each invidividual
            edge_distance1 = shared.data.dist_matrix()[currentNode][self.individual1[currentNode]]
            edge_distance2 = shared.data.dist_matrix()[currentNode][self.individual2[currentNode]]

            if edge_distance1 > edge_distance2:
                #if no loop is introduced proceed to save the edge in child
                if self.individual2[currentNode] not in visitedNodes:
                    child[currentNode] = self.individual2[currentNode]
                    visitedNodes.append(self.individual2[currentNode])
                    availableNodes.pop(self.individual2[currentNode])
                    currentNode = self.individual2[currentNode]
                else:
                    #if a loop would have been introduced try to generate a random edge
                    candidateNode = random.randint(0, len(self.individual1) - 1)
                    while(candidateNode not in availableNodes):
                        candidateNode = random.randint(0, len(self.individual1) - 1)
                    child[currentNode] = candidateNode
                    visitedNodes.append(candidateNode)
                    availableNodes.pop(candidateNode)
                    currentNode = candidateNode

            else:
                 #if no loop is introduced proceed to save the edge in child
                if self.individual1[currentNode] not in visitedNodes:
                    child[currentNode] = self.individual1[currentNode]
                    visitedNodes.append(self.individual1[currentNode])
                    availableNodes.pop(self.individual1[currentNode])
                    currentNode = self.individual1[currentNode]
                else:
                    #if a loop would have been introdued try to generate a random edge
                    candidateNode = random.randint(0, len(self.individual1) - 1)
                    while(candidateNode not in availableNodes):
                        candidateNode = random.randint(0, len(self.individual1) - 1)
                    child[currentNode] = candidateNode
                    visitedNodes.append(candidateNode)
                    availableNodes.pop(candidateNode)
                    currentNode = candidateNode
        return child


def cxEnhancedSCX(individual1, individual2):
    """
    Function that creates an instance of CXSCXCalculator and performs the simple SCX crossover

    """
    localHillClimbing = True
    child1 = CXSCXCalculator(individual1, individual2, shared.orderedSequenceOfNodes, localHillClimbing).crossover()
    child2 =  CXSCXCalculator(individual1, individual2, shared.orderedSequenceOfNodes, localHillClimbing).crossover()
    individual1[:] = child1[:]
    individual2[:] = child2[:]
    return individual1, individual2

def cxSimpleSCXMetaGA(individual1, individual2, n=3):
    """
    Function that creates an instance of CXSCXCalculator and performs the simple SCX crossover

    """
    localHillClimbing = False
    sequenceOfNodes = range(len(individual1))

    # Selecting the best crossing over over 'n' trials :
    best_score = 10**20
    for i in xrange(n):
        child1 = CXSCXCalculator(individual1, individual2, sequenceOfNodes, localHillClimbing).crossover()
        child2 =  CXSCXCalculator(individual2, individual1, sequenceOfNodes, localHillClimbing).crossover()
        score = shared.weight_matrix.score(child1) + shared.weight_matrix.score(child2)
        if score < best_score:
            best_child1, best_child2 = child1, child2

    individual1[:] = best_child1[:]
    individual2[:] = best_child2[:]
    return individual1, individual2

def cxSimpleSCX(individual1, individual2):
    """
    Function that creates an instance of CXSCXCalculator and performs the simple SCX crossover

    """
    localHillClimbing = False
    sequenceOfNodes = range(len(individual1))
    child1 = CXSCXCalculator(individual1, individual2, sequenceOfNodes, localHillClimbing).crossover()
    child2 =  CXSCXCalculator(individual2, individual1, sequenceOfNodes, localHillClimbing).crossover()
    individual1[:] = child1[:]
    individual2[:] = child2[:]
    return individual1, individual2


class CXSCXCalculator:

    """
    Contains the logic to perform sequential constructive crossover
    see: http://www.cscjournals.org/csc/manuscript/Journals/IJBB/volume3/Issue6/IJBB-41.pdf

    """

    def __init__(self, individual1, individual2, sequenceOfNodes, localHillClimbing):
        self.individual2 = individual2
        self.individual1 = individual1
        self.sequenceOfNodes = sequenceOfNodes
        self.localHillClimbing = localHillClimbing

    def crossover(self):
        """
        Computes the SCX crossover.

        """
        self.visitedNodes = []

        child = creator.Individual()

        #chose currentNodes randomly
        currentNode = self.individual1[random.randint(0, len(self.individual1) - 1)]
        child.append(currentNode)
        self.visitedNodes.append(currentNode)
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
            #if both individuals contain legit nodes, chose the one forming the edge
                legitNodeIn2 = None
            #with lowest cost
            if(legitNodeIn1 and legitNodeIn2):
                if shared.data.dist_matrix()[currentNode][legitNodeIn1] > shared.data.dist_matrix()[currentNode][legitNodeIn2]:
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
                sequentialNode = self._getSequentialNode(currentNode)
                child.append(sequentialNode)
                self.visitedNodes.append(sequentialNode)
                currentNode = sequentialNode
                if len(child) == len(self.individual1):
                    break

        return child

    def _getSequentialNode(self, currentNode):
        """
        get next non-visited node from the predefined sequenceOfNode
        """

        #simple optimisation to try to select with a 1/3 probability the closest node
        if self.localHillClimbing:
            a = random.random()
            if a < 1/3:
                closest = shared.data.dist_matrix()[currentNode][numpy.min(shared.data.dist_matrix()[currentNode]).index()]
                if closest not in self.visited and closest != currentNode:
                    return closest

        #otherwise assing a node from the predefined sequence of nodes
        for node in self.sequenceOfNodes:
            if (node not in self.visitedNodes) and (node != currentNode):
                return node
        return ValueError


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


    def crossover(self):
        child1 = self._createChild(self.individual1, self.individual2)
        child2 = self._createChild(self.individual2, self.individual1)
        self.individual1[:] = child1[:]
        self.individual2[:] = child2[:]

        return self.individual1, self.individual2

    def _createChild(self, individual1, individual2):

        self._buildEdgeMap(individual1, individual2)

        child = creator.Individual()
        #step1
        currentNode = individual1[random.randint(0, len(individual1) - 1)]
        while True:
            child.append(currentNode)
            #extract the nodes linked to current node
            neighborgs = self.edgeMap.pop(currentNode)
            neighborgs = list(neighborgs)
            #remove references to the current node
            self._cleanupNodeFromEdgeMap(currentNode)
            #then compute the next node if there are any
            if neighborgs != []:
                #find which neighborg node has the less edges
                currentNeighborg = neighborgs[0]
                currentLen = len(self.edgeMap[currentNeighborg])
                for neighborg in neighborgs[1:]:
                    if len(self.edgeMap[neighborg]) < currentLen:
                        #if this neighborg has less edges then keep him
                        currentLen = len(self.edgeMap[neighborg])
                        currentNeighborg = neighborg
                    elif len(self.edgeMap[neighborg]) == currentLen:
                        #if the neighborg has the same amout of edges
                        #break tie at random
                        if random.randint(0, 1) > 0.5:
                            #we keep the one we have
                            pass
                        else:
                            currentLen = len(self.edgeMap[neighborg])
                            currentNeighborg = neighborg
                    else:
                        #we keep the one we have
                        pass
                #the neighborg with the less edges is the next node in the child
                currentNode = currentNeighborg
            else:
                if self.edgeMap == {}:
                    break  # if there are no more nodes to assign then stop
                else:
                    #chose as next node any remaining node at random
                    currentNode = self.edgeMap.keys()[random.randint(0, len(self.edgeMap.keys()) - 1)]

        return child

    def _buildEdgeMap(self,individual1,individual2):
        """
        For each node looks at the corresponding edges in each individual and creates
        an edgeMap entry with as a set of neighboring nodes

        """
        self.edgeMap = {}
        for node in individual1:
            pos1 = individual1.index(node)
            pos2 = individual2.index(node)
            neighborg1 = individual1[(pos1 - 1) % len(individual1)]
            neighborg2 = individual1[(pos1 + 1) % len(individual1)]
            neighborg3 = individual2[(pos2 - 1) % len(individual2)]
            neighborg4 = individual2[(pos2 + 1) % len(individual2)]
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


__all__ = (cxNull,
           cxERX,
           cxHeuristic,
           cxSimpleSCX,
           cxEnhancedSCX,
           cxOrdered,
           cxPMX
           )
