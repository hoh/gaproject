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

    def toolbox(self, ind_size, operators):
        """Creating the toolbox.
        - operators : a dictionary of genetic operators
        - ind_size : the size of an individual for initialization
        """

        # Default values for the operators:
        all_operators = {
            'mate': tools.cxPartialyMatched,
            'mutate': (tools.mutShuffleIndexes, {'indpb': 0.05}),
            'select': (tools.selTournament, {'tournsize': 3}),
            'evaluate': None,  # This one MUST be implemented
            'indices': (random.sample, {'population': xrange(ind_size), 'k': ind_size}),
        }
        # Updating default values with operators
        for key in all_operators:
            if key in operators:
                all_operators[key] = operators[key]

        # Creating toolbox and populating it:
        toolbox = base.Toolbox()

        for key in all_operators:
            func = all_operators[key]

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

        # Structure initializers
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        return toolbox

    def stats(self):
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", tools.mean)
        stats.register("std", tools.std)
        stats.register("min", min)
        stats.register("max", max)
        return stats

    def run(self, algo, pop, toolbox, generations, population, cxpb, mutpb):

        hof = tools.HallOfFame(1)
        stats = self.stats()
        algo(pop, toolbox, cxpb, mutpb, generations, stats=stats, halloffame=hof)

        return pop, stats, hof
