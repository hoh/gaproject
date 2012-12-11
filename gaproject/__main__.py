#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

import sys
import pprint

from gaproject.data import Box
from gaproject.mydeap import MyDeap
from gaproject.analysis import plot
import gaproject.shared as shared

import gaproject.sets


def run(data, operators):
    '''Launches a run for the given dataset and genetic operators.
    '''
    # Running the DEAP:
    mydeap = MyDeap()
    toolbox = mydeap.toolbox(len(data), operators)
    pop, stats, hof = mydeap.run(toolbox, 100)

    print 'Best so far:', operators['evaluate'](hof[0])

    if shared.settings.plot:
        # Plotting the best result so far:
        plot(hof[0], data)

    # Returning results as a dictionary:
    fitness = operators['evaluate'](hof[0])
    return {'fitness': fitness,
            'best': hof[0],
            'operators': operators,
            }


def main():
    'Launches all runs.'

    box = Box('data/TSPBenchmark')
    data = box.get('belgiumtour.tsp')  # or xqf131.tsp
    shared.distance_map = data.dist_matrix()

    if shared.settings.plot:
        data.plot()

    results = {}

    sets = gaproject.sets.get()
    for b in sets:
        set_b = sets[b]
        operators = gaproject.sets.evaluate(set_b)

        result = run(data, operators)
        results[b] = result

        # 'average': numpy.average(scores),
        # 'std': numpy.std(scores),

    # Pretty printing the resulting scores:
    pprint.pprint(results)

if __name__ == '__main__':
    try:
        hof = main()
    except KeyboardInterrupt:
        print 'Execution stopped.'
