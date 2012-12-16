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

import deap.tools as tools
from deap.algorithms import varAnd


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

    return populations
