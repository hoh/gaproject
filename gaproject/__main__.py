#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

from gaproject.data import Box


def main():
    print 'Starting...'
    box = Box('data/TSPBenchmark')
    data = box.get('belgiumtour.tsp')
    print [i for i in data.positions()]

if __name__ == '__main__':
    main()
