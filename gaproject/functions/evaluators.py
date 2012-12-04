
'''
Here should come the fitness evaluation functions.
'''


class Evaluators(object):
    '''This class is used to allo a context for the evaluation functions
    such as access to the distance_map.'''

    def __init__(self, distance_map):
        self.distance_map = distance_map

    def evalTSP(self, individual):
        'The most basic evaluation, from the DEAP TSP example:'
        distance = self.distance_map[individual[-1]][individual[0]]
        for gene1, gene2 in zip(individual[0:-1], individual[1:]):
            distance += self.distance_map[gene1][gene2]
        return distance,
