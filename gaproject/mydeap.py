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

    def __init__(self):
        self.creator()

    def creator(self):
        "Setting up the creator."

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

        return creator

    def toolbox(self, ind_size, functions):
        """Creating the toolbox.
        - functions : a dictionary of genetic functions
        - ind_size : the size of an individual for initialization
        """

        # Default values for the functions:
        all_functions = {
            'mate': tools.cxPartialyMatched,
            'mutate': (tools.mutShuffleIndexes, {'indpb': 0.05}),
            'select': (tools.selTournament, {'tournsize': 3}),
            'evaluate': None,  # This one MUST be implemented
        }
        all_functions.update(functions)

        toolbox = base.Toolbox()

        # Attribute generator
        toolbox.register("indices", random.sample, xrange(ind_size), ind_size)

        # Structure initializers
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        for key in all_functions:
            func = all_functions[key]

            # Checking for wrong values:
            if func is None:
                raise ValueError('function cannot be null')

            # Extracting arguments if any:
            if type(func) in (list, tuple):
                func, args = func
            else:
                args = {}

            # Registration:
            toolbox.register(key, func, **args)

            # toolbox.register("mate", tools.cxPartialyMatched)
            # toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
            # toolbox.register("select", tools.selTournament, tournsize=3)
            # toolbox.register("evaluate", evaluator)

        return toolbox

    def stats(self):
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", tools.mean)
        stats.register("std", tools.std)
        stats.register("min", min)
        stats.register("max", max)
        return stats

    def run(self, toolbox, generations, population):
        random.seed(169)

        pop = toolbox.population(n=population)

        hof = tools.HallOfFame(1)
        stats = self.stats()

        algorithms.eaSimple(pop, toolbox, 0.7, 0.2, generations, stats=stats,
                            halloffame=hof)

        return pop, stats, hof
