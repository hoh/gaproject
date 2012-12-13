
"Module to analyze the result we've got. Eg: plot it."

import matplotlib.pyplot as plt

import gaproject.shared as shared
settings = shared.settings


def plot(individual, data):
    "Uses Matplotib to plot the nodes positions."

    positions = [data.positions[i] for i in individual]

    x_axis = [pos[0] for pos in positions]
    y_axis = [pos[1] for pos in positions]

    plt.plot(x_axis, y_axis, 'ro-')
    plt.show()


def fitness_plot(stats):
    '''Plots the stats object : fitness over generations.
    If a filename is given, will output the result in that file,
    else displays it on screen.
    '''
    def adjust(stats_list):
        'Transforms the list found in stats to a plottable list.'
        return [fit[0] for fit in stats_list[0]]

    plt.plot(adjust(stats.data['min']), 'b-')
    plt.plot(adjust(stats.data['max']), 'r-')
    plt.plot(adjust(stats.data['avg']), 'g-')
    plt.plot(adjust(stats.data['std']), 'y-')

    plt.show()


def analyse(results):
    import numpy

    for run in results:
        values = results[run]
        set_ = values['set']
        print
        print 'Run:', run
        print 'Fitness average:', numpy.average(values['fitness'])
        print 'Fitness std:', numpy.std(values['fitness'])
        print 'Generations:', settings.fallback(set_, 'generations')
        print 'Population:', settings.fallback(set_, 'population')
        print 'n =', len(values['fitness'])
        print
        # pprint.pprint(values)
