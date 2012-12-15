'''
Loop removal optimizer for TSP.
'''

import gaproject.shared as shared


def dist(node1, node2):
    return shared.data.dist_matrix()[node1][node2]


def loop_removal(function):
    '''To be used as a decorator on a function.
    Result will have 2-nodes loops removed.
    '''
    if shared.settings.loop_removal:
        def wrapped(*args, **kwargs):
            return remove_loops(function(*args, **kwargs))
        return wrapped
    else:
        return function


def remove_loops(individual):
    '''Removing 2-nodes loops from the individual by comparing
    the distance between a node and it's predecessor to the
    distance from the next node to it's follower and switching
    them if leads to an improvement.
    '''
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
