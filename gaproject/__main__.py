#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

import random

from gaproject.data import Box
from gaproject.mydeap import MyDeap
from gaproject.analysis import plot, analyse
from gaproject.store import Store
import gaproject.shared as shared
settings = shared.settings

import gaproject.sets


def run(data, operators):
    '''Launches a run for the given dataset and genetic operators.
    '''

    result = {'fitness': [],
              'best': [],
              }

    # Running the DEAP:
    mydeap = MyDeap()
    toolbox = mydeap.toolbox(len(data), operators)

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

        # Returning results as a dictionary:
        fitness = operators['evaluate'](hof[0])

        result['fitness'].append(fitness[0])
        result['best'].append(list(hof[0]))

    return result


def main():
    'Launches all runs.'

    box = Box('data/TSPBenchmark')
    data = box.get('belgiumtour.tsp')  # or belgiumtour.tsp
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
        analyse(results)

if __name__ == '__main__':
    try:
        hof = main()
    except KeyboardInterrupt:
        print 'Execution stopped.'
