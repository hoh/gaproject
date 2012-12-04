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
    #chose an individual randomly and insert it at a random position
    if(random.random()>indpb):
        indexRandomNode = random.randint(0, len(individual)-1)
        insertionPoint = random.randint(0, len(individual)-1)
        removedValue=individual.pop(indexRandomNode)  
        individual.insert(insertionPoint,removedValue)
    return individual

def inversionMutation(individual,indpb):
    #chose a Subtour then insert it at a different part of the individual
    if(random.random()>indpb):
        #compute the beginning and end of the Subtour.
        begSubtour = random.randint(0, len(individual)-1)
        endSubtour = random.randint(begSubtour, len(individual)-1)

        #print begSubtour , endSubtour

        #save the Subtour
        Subtour = individual[begSubtour:endSubtour]

        #remove it from individual
        del individual[begSubtour:endSubtour]

        #compute where to insert it
        insertionPos = random.randint(0, len(individual)-1)

        #create the new individual by inserting the Subtour
        individual[:] = individual[0:insertionPos] + Subtour + individual[insertionPos:]

    return individual

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

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", inversionMutation, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalTSP)


#def simpleInversionMutation(individual):

def main():
    random.seed(169)

    pop = toolbox.population(n=300)

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
