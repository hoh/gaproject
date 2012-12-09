#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

from gaproject.data import Box
from gaproject.mydeap import MyDeap
from gaproject.analysis import plot

from gaproject.functions.evaluators import Evaluators
from gaproject.functions.mutators import mutShuffleIndexes, \
                                         insertionMutation, \
                                         inversionMutation, \
                                         simpleInversionMutation


def run(data, operators):
    'Launches a run for the given dataset and genetic operators'
    # Running the DEAP:
    mydeap = MyDeap()
    toolbox = mydeap.toolbox(len(data), operators)
    pop, stats, hof = mydeap.run(toolbox)

    print 'Best so far:', operators['evaluate'](hof[0])
    # Plotting the best result so far:
    plot(hof[0], data)


def main():
    'Launches all runs.'

    box = Box('data/TSPBenchmark')
    data = box.get('belgiumtour.tsp')  # or xqf131.tsp
    data.plot()

    distance_map = data.dist_matrix()

    operators = {'evaluate': Evaluators(distance_map).evalTSP,

                 #'mutate': (mutShuffleIndexes, {'indpb': 0.05}),
                 'mutate': (insertionMutation, {'indpb': 0.05}),
                 #'mutate': (inversionMutation, {'indpb': 0.05}),
                 #'mutate': (simpleInversionMutation, {'indpb': 0.05}),
                 }

    run(data, operators)

    operators = {'evaluate': Evaluators(distance_map).evalTSP,

                 'mutate': (mutShuffleIndexes, {'indpb': 0.05}),
                 #'mutate': (insertionMutation, {'indpb': 0.05}),
                 #'mutate': (inversionMutation, {'indpb': 0.05}),
                 #'mutate': (simpleInversionMutation, {'indpb': 0.05}),
                 }

    run(data, operators)

if __name__ == '__main__':
    try:
        hof = main()
    except KeyboardInterrupt:
        print 'Execution stopped.'
