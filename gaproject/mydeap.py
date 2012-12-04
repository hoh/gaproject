'''
Generic setup for DEAP in this project.
'''

import array
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


class MyDeap(object):
    "Class for generic setup of DEAP in our problem."

    def creator(self):
        "Setting up the creator."

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

        return creator

    def toolbox(self, ind_size, evaluator):
        "Creating the toolbox."

        toolbox = base.Toolbox()

        # Attribute generator
        toolbox.register("indices", random.sample, xrange(ind_size), ind_size)

        # Structure initializers
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("mate", tools.cxPartialyMatched)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("evaluate", evaluator)

        return toolbox

    def stats(self):
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", tools.mean)
        stats.register("std", tools.std)
        stats.register("min", min)
        stats.register("max", max)
        return stats

    def run(self, toolbox):
        random.seed(169)

        pop = toolbox.population(n=300)

        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", tools.mean)
        stats.register("std", tools.std)
        stats.register("min", min)
        stats.register("max", max)

        algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 2000, stats=stats,
                            halloffame=hof)

        return pop, stats, hof
