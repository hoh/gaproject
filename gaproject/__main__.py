#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

from sys import argv

import gaproject.run
from gaproject.tools.results import Results


class Main(object):
    '''Main run function. Added method become automatically available from
    the command line.
    '''

    def __init__(self):
        'Launches the main execution.'
        if 'help' in argv or len(argv) == 1:
            self._print_help()
        else:
            for i in argv:
                if hasattr(self, i):
                    getattr(self, i)()

    def _print_help(self):
        'Prints all available actions.'
        print('usage:')
        for method in dir(self):
            if not method.startswith('_'):
                print('  {} - {}'.format(method, getattr(self, method).__doc__))

    def run(self):
        'Launches the banchmarks.'
        return gaproject.run.main()

    def flush(self):
        'Deletes all results from the database.'
        s = gaproject.store.Store()
        s.runs.remove({})

    def results(self):
        'Prints and plots the results.'
        results = Results()
        results.print_()
        results.plot()


if __name__ == '__main__':
    Main()
