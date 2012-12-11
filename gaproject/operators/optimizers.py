'''
Loop removal optimizer for TSP.
'''

import gaproject.shared as shared


def dist(node1, node2):
    return shared.distance_map[node1][node2]


def remove_loops(individual):

    for i in xrange(1, len(individual) - 2):
        d1 = dist(individual[i - 1], individual[i]) \
           + dist(individual[i + 1], individual[i + 2])
        d2 = dist(individual[i - 1], individual[i + 1]) \
           + dist(individual[i], individual[i + 2])

        if d2 < d1:
            individual[i], individual[i + 1] = individual[i + 1], individual[i]

    return individual
