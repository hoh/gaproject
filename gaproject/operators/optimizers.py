'''
Loop removal optimizer for TSP.
'''

import gaproject.shared as shared


def dist(node1, node2):
    return shared.distance_map[node1][node2]


def loop_removal(function):
    if shared.settings.loop_removal:
        def wrapped(*args, **kwargs):
            return remove_loops(function(*args, **kwargs))
        return wrapped
    else:
        return function


def remove_loops(individual):
    length = len(individual)

    for i in xrange(len(individual)):

        before = (i - 1) % length
        next = (i + 1) % length
        after = (i + 2) % length

        d1 = dist(individual[before], individual[i]) \
           + dist(individual[next], individual[after])
        d2 = dist(individual[before], individual[next]) \
           + dist(individual[i], individual[after])

        if d2 < d1:
            individual[i], individual[next] = individual[next], individual[i]

    return individual
