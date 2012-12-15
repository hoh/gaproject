#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

from sys import argv
import json

import gaproject.run
from gaproject.data import Box
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
        'Launches the benchmarks.'
        box = Box('data/TSPBenchmark')
        data = box.get('xqf131.tsp')
        # Overwriting data file if given:
        for arg in argv:
            print arg
            if box.isfile(arg):
                data = box.get(arg)
        print 'Using benchmark:', data.path
        return gaproject.run.main(data)

    def flush(self):
        'Deletes all results from the database.'
        s = gaproject.store.Store()
        s.runs.remove({})

    def results(self):
        'Prints and plots the results.'
        results = Results()
        results.print_()
        results.plot()

    def queue(self):
        'Loads jobs fron a JSON file and adds them to the queue.'
        # Loading file:
        filename = argv[argv.index('queue') + 1]
        new_jobs = json.load(open(filename), encoding='utf-8')
        # Adding to DB queue:
        s = gaproject.store.Store()
        for job in new_jobs:
            s.jobs.add(job)

    def unqueue(self):
        "Deletes all jobs from the database's queue."
        s = gaproject.store.Store()
        s.jobs.remove({})


if __name__ == '__main__':
    Main()
