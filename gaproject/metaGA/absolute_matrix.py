'Absolute matrix'

class WeightMatrix(object):
    '''This class is used to store and retrieve weights between two nodes.

    At the moment, it uses a dictionnary to store the nodes.
    '''

    def __init__(self, size):
        self._couples = {}
        self._size = size
        # _max_size = number of possible combinations:
        self._max_size = ((self._size ** 2) - self._size) / 2

    def __getitem__(self, couple):
        '''Returns the weight for the given two nodes, in any order.
        Defaults to zero.
        '''
        return self._couples.get(couple, 1)

    def __contains__(self, couple):
        return couple in self._couples

    def __setitem__(self, couple, weight):
        self._couples[couple] = weight

    def __delitem__(self, couple):
        del self._couples[couple]

    def add(self, vector):
        '''Updates the weights matrix from the values of the vector.

        At the moment, gives a weight of then size of the vector and
        sums up over all iterations.'''
        size = len(vector)
        for i in xrange(size - 1):
            couple = tuple(sorted((vector[i], vector[i + 1])))
            # Counting the number of times:
            if couple in self:
                self[couple] += 1
            else:
                self[couple] = 1
        # for couple in combinations(vector, 2):
        #     if couple in self:
        #         self[couple] += len(vector)
        #     else:
        #         self[couple] = len(vector)

    # def scale(self):
    #     '''Returns a scaling factor for the weight matrix, namely
    #     the size of an individual divided by probability for each node.
    #     '''
    #     # Summ of value for couples present:
    #     sum_factors = sum(self.weight(n) for n in self._couples)
    #     # 1 * number of couples not present:
    #     sum_rest = (self._max_size - len(self._couples))

    #     return float(self._max_size) / (sum_factors + sum_rest)

    def weight(self, couple, unsorted=False):
        '''Returns a probability associated to the given couple.
        Has to be sorted or give 'unserted=True'.
        '''
        if unsorted:
            couple = tuple(sorted(couple))

        if couple in self and self[couple] >= 3:
            count = self[couple]
            weight = 0
        else:
            weight = 1

        return weight
        # w = 1. / self[couple]
        # return w
        # return 1 - ((1 - w) ** 0.5)

    def scaled_weight(self, couple, unsorted=False):
        '''Returns a probability associated to the given couple.
        Has to be sorted or give 'unserted=True'.
        '''
        if unsorted:
            couple = tuple(sorted(couple))

        def scale(value):
            return (1. / value) ** 0.5

        return scale(self[couple])

    def node_weight(self, node, ind):
        '''Computes the weight of removing the given node from the
        given individual. Product of weight of link with previous node
        and link with the next node.
        '''
        i = ind.index(node)
        couple1 = (ind[i - 1], node)
        couple2 = (ind[(i + 1) % len(ind)], node)

        w = self.weight(couple1, unsorted=True) \
          * self.weight(couple2, unsorted=True)
        return w

    def choice(self, ind):
        '''Pseudo-randomly choses a node from the individual, depending
        on the weight matrix.
        '''
        # Selecting via roulette wheel:
        weights = [self.node_weight(node, ind) for node in ind]
        pick = random.uniform(0, sum(weights))
        current = 0
        for i in xrange(len(ind)):
            node = ind[i]
            current += weights
            if current > pick:
                return node

    def next_to(self, node):
        '''Returns a list of nodes in the order of probability they would
        appear after the given node.
        '''
        results = []
        for key in self._couples:
            if node in key:
                other_node = key[0] if key[0] != node else key[1]
                weight = self.weight((node, other_node), unsorted=True)
                results.append((other_node, weight))
        return sorted(results, key=lambda x: x[1])

    def score(self, ind):
        ''' Evaluates the 'connectivity score' for the given individual. Function
        of the number of couples found.
        '''
        weights = [self.node_weight(node, ind) for node in ind]
        return sum(weights)