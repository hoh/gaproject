
"Module to analyze the result we've got. Eg: plot it."

import gaproject.shared as shared
settings = shared.settings


def plot(individual, data):
    "Uses Matplotib to plot the nodes positions."

    positions = [data.positions[i] for i in individual]

    x_axis = [pos[0] for pos in positions]
    y_axis = [pos[1] for pos in positions]

    import matplotlib.pyplot as plt
    plt.plot(x_axis, y_axis, 'ro-')
    plt.show()


def fitness_plot(stats):
    import matplotlib.pyplot as plt

    data_min = [fit[0] for fit in stats.data['min'][0]]
    # import pdb; pdb.set_trace()
    plt.plot(data_min)
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
