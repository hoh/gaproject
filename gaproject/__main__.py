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


def main():
    box = Box('data/TSPBenchmark')
    data = box.get('xqf131.tsp')  # or belgiumtour.tsp

    # data.plot()

    distance_map = data.dist_matrix()

    functions = {'evaluate': Evaluators(distance_map).evalTSP,

                 #'mutate': (mutShuffleIndexes, {'indpb': 0.05}),
                 'mutate': (insertionMutation, {'indpb': 0.05}),
                 #'mutate': (inversionMutation, {'indpb': 0.05}),
                 #'mutate': (simpleInversionMutation, {'indpb': 0.05}),


                 }

    # Running the DEAP:
    mydeap = MyDeap()
    toolbox = mydeap.toolbox(len(data), functions)
    pop, stats, hof = mydeap.run(toolbox)

    # Plotting the best result so far:
    plot(hof[0], data)


if __name__ == '__main__':
    try:
        hof = main()
    except KeyboardInterrupt:
        print 'Execution stopped.'
