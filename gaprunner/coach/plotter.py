'''
Used in the Queue system to plot results.

'''

import json
import os.path

import matplotlib.pyplot as plt
from gaproject.data import Box
import gaproject.shared as shared


def plot_ind(individual, data):
    "Uses Matplotib to plot the nodes positions."

    positions = [data.positions[i] for i in individual]

    x_axis = [pos[0] for pos in positions]
    y_axis = [pos[1] for pos in positions]

    plt.figure()
    plt.title('Best individual')
    plt.plot(x_axis, y_axis, 'ro-')
    plt.show(block=False)


def plot_fitness(stats):
    '''Plots the stats object : fitness over generations.
    If a filename is given, will output the result in that file,
    else displays it on screen.
    '''
    def adjust(stats_list):
        'Transforms the list found in stats to a plottable list.'
        return [fit[0] for fit in stats_list[0]]

    plt.figure()
    plt.plot(adjust(stats['min']), 'b-')
    plt.plot(adjust(stats['max']), 'r-')
    plt.plot(adjust(stats['avg']), 'g-')
    plt.plot(adjust(stats['std']), 'y-')

    plt.show(block=False)


def plot(job):
    job_result_path = os.path.join(shared.settings.filesDir, str(job['_id']), 'data.json')
    job_result = json.load(open(job_result_path))

    box = Box('data/TSPBenchmark')
    data = box.get(job['data'])

    best_individual = job_result['best'][0]
    plot_ind(best_individual, data)

    for stats in job_result['stats']:
        plot_fitness(stats)

    raw_input('end ?')
    plt.close()
    plt.close()
