
from numpy import average, std

from prettytable import PrettyTable
from gaproject.store import Store

import matplotlib.pyplot as plt


class RunTable(PrettyTable):

    def __init__(self):
        PrettyTable.__init__(self,
            field_names=['name', 'n', 'fit avg', 'fit std', 'pop', 'gen', 'mutator', 'cx']
            )

    def add_run(self, run):
        self.add_row([
            run['set']['name'],
            len(run['fitness']),
            average(run['fitness']),
            std(run['fitness']),
            run['set']['population'],
            run['set']['generations'],
            run['set'].get('mutate', [''])[0],
            run['set'].get('mate', ''),
            ])


class Results(object):

    def __init__(self):
        self.s = Store()

    def find(self, filter={}):
        return self.s.runs.find(filter)

    def find_one(self, filter={}):
        return self.s.runs.find_one(filter)

    def add_run(self, table, run):
        'Prints a certain run.'
        table.add_row([
            run['set']['name'],
            len(run['fitness']),
            average(run['fitness']),
            std(run['fitness']),
            run['set']['population'],
            run['set']['generations'],
            run['set'].get('mutate', [''])[0],
            run['set'].get('mate', ''),
            ])

    def print_(self):
        '''Prints all elements in the DB (limiting printed keys to a subset).
        '''

        table = RunTable()

        for run in self.find():
            table.add_run(run)

        print table

    def plot(self):
        ''' Generates plots for results in the DB.
        '''

        def adjust(stats_list):
            'Transforms the list found in stats to a plottable list.'
            return [fit[0] for fit in stats_list[0]]

        for run in self.find():
            for data in run['stats']:
                data = adjust(data['min'])
                plt.plot(data, 'b-')

            # Plotting average:
            plt.plot(
                [average([adjust(data['min'])[i]
                          for data in run['stats']])
                 for i in xrange(len(data))],
                'r-')

            plt.title(run['set']['name'])
            plt.xlabel('Generations')
            plt.ylabel('Min. fitness')
            plt.show()


