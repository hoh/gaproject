#    Source: http://deap.googlecode.com/hg/examples/ga_tsp.py

#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import random
import json

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

def insertionMutation(individual,indpb):
    """
    chose an individual randomly and insert it at a random position
    """
    if(random.random()>indpb):
        indexRandomNode = random.randint(0, len(individual)-1)
        insertionPoint = random.randint(0, len(individual)-1)
        removedValue=individual.pop(indexRandomNode)  
        individual.insert(insertionPoint,removedValue)
    return individual

def inversionMutation(individual,indpb):
    """
    chose a Subtour then insert it reversed at a different part of the individual
    """
    if(random.random()>indpb):
        #compute the beginning and end of the Subtour.
        begSubtour = random.randint(0, len(individual)-1)
        endSubtour = random.randint(begSubtour, len(individual)-1)

        #extract the Subtour and reverse it
        Subtour = individual[begSubtour:endSubtour]
        Subtour.reverse()

        #remove Subtour from individual
        del individual[begSubtour:endSubtour]

        #compute where to insert it
        insertionPos = random.randint(0, len(individual)-1)

        #create the new individual by inserting the Subtour at the insertion position
        individual[:] = individual[0:insertionPos] + Subtour + individual[insertionPos:]

    return individual

def simpleInversionMutation(individual, indpb):
    """
    chose a Subtour then reverse it at a different part of the individual
    """
    if(random.random()>indpb):
        begSubtour = random.randint(0, len(individual)-1)
        endSubtour = random.randint(begSubtour, len(individual)-1)

        #extract the Subtour
        Subtour = individual[begSubtour:endSubtour]
        Subtour.reverse()

        #create the new individual
        individual[:] = individual[0:begSubtour] + Subtour + individual[endSubtour:]

    return individual

def cxERX(individual1,individual2):
    """
    ERX performs a crossover that tries to pass to the next generation the common edges of the parents.
    ERX returns one individual only.
    """
    edgeMap = {}
    #build the edgemap
    for node in individual1:
        pos1 = individual1.index(node)
        pos2 = individual2.index(node)
        neighborg1 = individual1[(pos1-1) % len(individual1)]
        neighborg2 = individual1[(pos1+1) % len(individual1)]
        neighborg3 = individual2[(pos2-1) % len(individual2)]
        neighborg4 = individual2[(pos2+1) % len(individual2)]
        edgeMap[node]=set([neighborg1,neighborg2,neighborg3,neighborg4])

    child = creator.Individual()
    #step1
    currentNode = individual1[random.randint(0,len(individual1)-1)]
    while True:
        child.append(currentNode)
        #extract the nodes linked to current node
        neighborgs = edgeMap.pop(currentNode)
        neighborgs = list(neighborgs)
        #remove references to the current node
        cleanupNodeFromEdgeMap(edgeMap, currentNode)
        if neighborgs != []:
            #find which neighborg node has the less edges
            currentNeighborg = neighborgs[0]
            currentLen = len(edgeMap[currentNeighborg])
            for neighborg in neighborgs:
                if len(edgeMap[neighborg]) < currentLen:
                    currentLen = len(edgeMap[neighborg])
                    currentNeighborg = neighborg
            #the neighborg with the less edges is the next node in the child
            currentNode = currentNeighborg
        else:
            if edgeMap == {}: 
                break #if there are no more nodes to assign then stop
            else:
                #chose as next node any remaining node at random
                currentNode = edgeMap.keys()[random.randint(0,len(edgeMap.keys())-1)]
    return child

def cleanupNodeFromEdgeMap(edgeMap,referenceNode):
    edgeMapEntriesToBeRemoved = []
    for node in edgeMap:
        if referenceNode in edgeMap[node]:
            edgeMap[node].remove(referenceNode)
        if edgeMap[node] == set():
            edgeMapEntriesToBeRemoved.append(node)
    for node in edgeMapEntriesToBeRemoved:
            edgeMapEntriesToBeRemoved.remove(node)

# gr*.json contains the distance map in list of list style in JSON format
tsp = json.load(open("gr17.json", "r"))
distance_map = tsp["DistanceMatrix"]
IND_SIZE = tsp["TourSize"]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("indices", random.sample, xrange(IND_SIZE), IND_SIZE)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalTSP(individual):
    distance = distance_map[individual[-1]][individual[0]]
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += distance_map[gene1][gene2]
    return distance,

toolbox.register("mate", cxERX)
toolbox.register("mutate", simpleInversionMutation, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalTSP)

def main():

    # ind1 = creator.Individual()
    # ind2 = creator.Individual()
    # ind1[:] = array.array('i',[1,2,3,4,5,6,7,8,9])
    # ind2[:] = array.array('i',[4,1,2,8,7,6,9,3,5]) 
    # print cxERX(ind1,ind2)

    random.seed(169)
    
    pop = toolbox.population(n=500)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    stats.register("std", tools.std)
    stats.register("min", min)
    stats.register("max", max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 40, stats=stats,
                        halloffame=hof)

    return pop, stats, hof

if __name__ == "__main__":
    main()
