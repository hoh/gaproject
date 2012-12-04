#!/usr/bin/env python

'''
This is the main file of the project, used to setup and launch the computation.
'''

from gaproject.data import Box


def main():
    print 'Starting...'
    box = Box('data/TSPBenchmark')
    data = box.get('belgiumtour.tsp')

if __name__ == '__main__':
    main()
