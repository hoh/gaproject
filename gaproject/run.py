'''
Main functions to run the genetic algorighms and benchmarks.
'''

import random

from gaproject.data import Box
from gaproject.mydeap import MyDeap
from gaproject.analysis import plot, analyze, fitness_plot
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

    for repetition in xrange(repetitions):
        random.seed(100 + repetition)

        pop, stats, hof = mydeap.run(toolbox,
                                     generations,
                                     population)

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


def main():
    'Launches all runs.'

    box = Box('data/TSPBenchmark')
    data = box.get('xqf131.tsp')  # or belgiumtour.tsp
    shared.distance_map = data.dist_matrix()
    shared.orderedSequenceOfNodes = data.nodesOrderedByMedian(shared.distance_map)

    if shared.settings.plot:
        data.plot()

    # Initializing results gatherer:
    if settings.use_db:
        store = Store()
    else:
        results = {}

    sets = gaproject.sets.get()
    for b in sets:
        set_b = sets[b]

        operators = gaproject.sets.evaluate(set_b)
        result = run(data, operators)
        result['set'] = set_b

        # Puting results in chose output:
        if settings.use_db:
            store.runs.insert(result)
        else:
            results[b] = result

        # 'average': numpy.average(scores),
        # 'std': numpy.std(scores),

    # Pretty printing the resulting scores:
    if not settings.use_db:
        analyze(results)
