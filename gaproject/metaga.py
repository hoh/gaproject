'''

Implementation of Meta Genetic Algorithms.

This is inspired by M. Milinkovitch's lesson of Evolutive Biology, ULB 2007.

The main idea is to focus evolution on characters that have a lower probability
to participate to a high fitness. This is done by comparing individuals in
different independently created subpopulations, and assigning a lower mutation
probability to sequences of characters appearing in different populations
through evolution.

The function below is based on DEAP's deap.algorithms.eaSimple and fitted to
the needs of the current problem.
'''

from difflib import SequenceMatcher
from itertools import combinations, chain

from operator import attrgetter

import deap.tools as tools
from deap.algorithms import varAnd

import gaproject.shared as shared


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
        for couple in combinations(vector, 2):
            if couple in self:
                self[couple] += len(vector)
            else:
                self[couple] = len(vector)

    def scale(self):
        '''Returns a scaling factor for the weight matrix, namely
        the size of an individual divided by probability for each node.
        '''
        # Summ of value for couples present:
        sum_factors = sum([(1. / n) for n in self._couples.values()])
        # 1 * number of couples not present:
        sum_rest = (self._max_size - len(self._couples))

        return float(self._max_size) / (sum_factors + sum_rest)

    def weight(self, couple, unsorted=False):
        '''Returns a probability associated to the given couple.
        '''
        if unsorted:
            couple = tuple(sorted(couple))
        return 1. / self[couple]


def eaMeta(populations, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm implements MetaGA and compares individuals in
    subpopulations to direct the mutations.

    :param population: A list of populations of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population.

    It uses :math:`\lambda = \kappa = \mu` and goes as follow.
    It first initializes the population (:math:`P(0)`) by evaluating
    every individual presenting an invalid fitness. Then, it enters the
    evolution loop that begins by the selection of the :math:`P(g+1)`
    population. Then the crossover operator is applied on a proportion of
    :math:`P(g+1)` according to the *cxpb* probability, the resulting and the
    untouched individuals are placed in :math:`P'(g+1)`. Thereafter, a
    proportion of :math:`P'(g+1)`, determined by *mutpb*, is
    mutated and placed in :math:`P''(g+1)`, the untouched individuals are
    transferred :math:`P''(g+1)`. Finally, those new individuals are evaluated
    and the evolution loop continues until *ngen* generations are completed.
    Briefly, the operators are applied in the following order ::

        evaluate(population)
        for i in range(ngen):
            offspring = select(population)
            offspring = mate(offspring)
            offspring = mutate(offspring)
            evaluate(offspring)
            population = offspring

    This function expects :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.

    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """

    shared.weight_matrix = WeightMatrix(size=len(populations[0][0]))

    for population in populations:
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if halloffame is not None:
            halloffame.update(population)
        if stats is not None:
            stats.update(population)
        if verbose:
            column_names = ["gen", "evals"]
            if stats is not None:
                column_names += stats.functions.keys()
            logger = tools.EvolutionLogger(column_names)
            logger.logHeader()
            logger.logGeneration(evals=len(population), gen=0, stats=stats)

    # Begin the generational process
    for gen in xrange(1, ngen + 1):

        for population in populations:
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population))

            # Variate the pool of individuals
            offspring = varAnd(offspring, toolbox, cxpb, mutpb)

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(offspring)

            # Replace the current population by the offspring
            population[:] = offspring

            # Update the statistics with the new population
            if stats is not None:
                stats.update(population)

            if verbose:
                logger.logGeneration(evals=len(invalid_ind), gen=gen, stats=stats)

        # ===== MetaGA part: updating mutation probabilities =====

        # List of best individuals:
        best_individuals = [sorted(pop, key=attrgetter("fitness"), reverse=True)[0]
                            for pop in populations]

        shared.weight_matrix = WeightMatrix(size=shared.data.size())
        # Computing matches for every combination of individuals:
        for i0, i1 in combinations(best_individuals, 2):

            # Computing matches and reverse-matches:
            matcher = SequenceMatcher(None, i0, i1)
            matches = [i for i in matcher.get_matching_blocks() if i.size > 1]
            # Reverting one of the individuals:
            reverse_matcher = SequenceMatcher(None, i0[::-1], i1)
            reverse_matches = [i for i in reverse_matcher.get_matching_blocks() if i.size > 1]

            # Adding all matches to the weight matrix:
            for m in chain(matches, reverse_matches):
                nodes = tuple(i0[m.a:(m.a + m.size)])
                shared.weight_matrix.add(nodes)

        print 'L', len(shared.weight_matrix._couples), sum(shared.weight_matrix._couples.values())
        print 'S', shared.weight_matrix.scale()

    return populations
