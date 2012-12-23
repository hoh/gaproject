'''
Main functions to run the genetic algorighms and benchmarks.
'''

import random

from deap import algorithms

from gaproject.mydeap import MyDeap
import gaproject.metaga as metaga


# Loading settings:
import gaproject.shared as shared
settings = shared.settings

if settings.plot:
    from gaproject.analysis import plot, fitness_plot


def run(data, operators):
    '''Launches a run for the given dataset and genetic operators.
    '''

    result = {'fitness': [],
              'best': [],
              'stats': [],
              }

    # Running the DEAP:
    mydeap = MyDeap()
    toolbox = mydeap.toolbox(len(data), operators)

    # Getting main parameters from operators of default from settings:
    population = operators['population']
    generations = operators['generations']
    repetitions = operators['repetitions']
    cxpb = operators['cxpb']
    mutpb = operators['mutpb']

    for repetition in xrange(repetitions):
        random.seed(100 + repetition)

        if settings.metaGA in (False, 0, 1):
            pop = toolbox.population(n=population)
            algo = algorithms.eaSimple
            pop, stats, hof = mydeap.run(algo,
                                         pop,
                                         toolbox,
                                         generations,
                                         population,
                                         cxpb,
                                         mutpb)
        else:
            pops = [toolbox.population(n=population) for i in xrange(settings.metaGA)]
            algo = metaga.eaMeta
            pop, stats, hof = mydeap.run(algo,
                                         pops,
                                         toolbox,
                                         generations,
                                         population,
                                         cxpb,
                                         mutpb)

        print 'Best so far:', operators['evaluate'](hof[0])

        if settings.plot:
            # Plotting the best result so far:
            plot(hof[0], data)
            fitness_plot(stats)

        # Returning results as a dictionary:
        fitness = operators['evaluate'](hof[0])

        result['fitness'].append(fitness[0])
        result['best'].append(list(hof[0]))
        result['stats'].append(stats.data)

    return result
