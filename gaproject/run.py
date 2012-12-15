'''
Main functions to run the genetic algorighms and benchmarks.
'''

import random

from gaproject.mydeap import MyDeap
from gaproject.analysis import plot, fitness_plot
from gaproject.store import Store
import gaproject.sets

# Loading settings:
import gaproject.shared as shared
settings = shared.settings


def run(data, operators):
    '''Launches a run for the given dataset and genetic operators.
    '''

    result = {'fitness': [],
              'best': [],
              'stats': [],
              }

    # Running the DEAP:
    mydeap = MyDeap()
    toolbox = mydeap.toolbox(len(data), operators)

    # Getting main parameters from operators of default from settings:
    population = settings.fallback(operators, 'population')
    generations = settings.fallback(operators, 'generations')
    repetitions = settings.fallback(operators, 'repetitions')
    cxpb = settings.fallback(operators, 'cxpb')
    mutpb = settings.fallback(operators, 'mutpb')

    for repetition in xrange(repetitions):
        random.seed(100 + repetition)

        pop, stats, hof = mydeap.run(toolbox,
                                     generations,
                                     population,
                                     cxpb,
                                     mutpb)

        print 'Best so far:', operators['evaluate'](hof[0])

        if shared.settings.plot:
            # Plotting the best result so far:
            plot(hof[0], data)
            fitness_plot(stats)

        # Returning results as a dictionary:
        fitness = operators['evaluate'](hof[0])

        result['fitness'].append(fitness[0])
        result['best'].append(list(hof[0]))
        result['stats'].append(stats.data)

    return result


def main(data):
    'Launches all runs.'

    shared.data = data
    shared.orderedSequenceOfNodes = data.nodesOrderedByMedian(shared.data.dist_matrix())

    if shared.settings.plot:
        data.plot()

    store = Store()

    sets = gaproject.sets.get()
    for set_ in sets:
        print 'Running set:', set_

        operators = gaproject.sets.evaluate(set_)
        result = run(data, operators)
        result['set'] = set_

        # Puting results in DB:
        store.runs.insert(result)
