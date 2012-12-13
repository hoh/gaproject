
from numpy import average, std

from prettytable import PrettyTable
from gaproject.store import Store

import matplotlib.pyplot as plt


class Results(object):

    def __init__(self):
        self.s = Store()

    def print_(self):
        '''Prints all elements in the DB (limiting printed keys to a subset).
        '''

        table = PrettyTable([
            'name', 'fitness', 'population', 'generations'
            ])

        for run in self.s.runs.find():
            table.add_row([
                run['set']['name'],
                run['fitness'],
                run['set']['population'],
                run['set']['generations'],
                ])

        print table

    def plot(self):
        ''' Generates plots for results in the DB.
        '''

        def adjust(stats_list):
            'Transforms the list found in stats to a plottable list.'
            return [fit[0] for fit in stats_list[0]]

        for run in self.s.runs.find():
            for data in run['stats']:
                data = adjust(data['min'])
                plt.plot(data, 'b-')

            # Plotting average:
            plt.plot(
                [average([adjust(data['min'])[i]
                          for data in run['stats']])
                 for i in xrange(len(data))],
                'r-')

            plt.show()


