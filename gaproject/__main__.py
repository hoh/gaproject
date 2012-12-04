#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

from gaproject.data import Box
from gaproject.mydeap import MyDeap


def main():
    print 'Starting...'
    box = Box('data/TSPBenchmark')
    # data = box.get('belgiumtour.tsp')
    data = box.get('xqf131.tsp')
    # print data.positions
    # print data.dist_matrix()
    # print len(data)

    distance_map = data.dist_matrix()

    def evalTSP(individual):
        distance = distance_map[individual[-1]][individual[0]]
        for gene1, gene2 in zip(individual[0:-1], individual[1:]):
            distance += distance_map[gene1][gene2]
        return distance,

    mydeap = MyDeap()
    print mydeap.creator()
    print mydeap.toolbox(len(data), evalTSP)

    toolbox = mydeap.toolbox(len(data), evalTSP)

    pop, stats, hof = mydeap.run(toolbox)


if __name__ == '__main__':
    main()
