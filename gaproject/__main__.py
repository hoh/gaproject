#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

import random

from gaproject.data import Box
from gaproject.mydeap import MyDeap
from gaproject.analysis import plot, analyse
import gaproject.shared as shared

import gaproject.sets


def run(data, operators):
    '''Launches a run for the given dataset and genetic operators.
    '''

    result = {'fitness': [],
              'best': [],
              'operators': operators}

    # Running the DEAP:
    mydeap = MyDeap()
    toolbox = mydeap.toolbox(len(data), operators)

    for repetition in xrange(shared.settings.repetitions):
        random.seed(100 + repetition)

        pop, stats, hof = mydeap.run(toolbox,
                                     shared.settings.generations,
                                     shared.settings.population)

        print 'Best so far:', operators['evaluate'](hof[0])

        if shared.settings.plot:
            # Plotting the best result so far:
            plot(hof[0], data)

        # Returning results as a dictionary:
        fitness = operators['evaluate'](hof[0])

        result['fitness'].append(fitness[0])
        result['best'].append(hof[0])

    return result


def main():
    'Launches all runs.'

    box = Box('data/TSPBenchmark')
    data = box.get('xqf131.tsp')  # or belgiumtour.tsp
    shared.distance_map = data.dist_matrix()

    if shared.settings.plot:
        data.plot()

    results = {}

    sets = gaproject.sets.get()
    for b in sets:
        set_b = sets[b]

        operators = gaproject.sets.evaluate(set_b)
        results[b] = run(data, operators)

        # 'average': numpy.average(scores),
        # 'std': numpy.std(scores),

    # Pretty printing the resulting scores:
    analyse(results)

if __name__ == '__main__':
    try:
        hof = main()
    except KeyboardInterrupt:
        print 'Execution stopped.'
