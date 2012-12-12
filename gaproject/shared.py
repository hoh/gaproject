'''
Empty module used to store global objects within GAPROJECT.
'''

import sys


class Settings(object):

    def __init__(self):
        self.plot = 'plot' in sys.argv
        self.generations = 200
        self.population = 100
        self.loop_removal = True
        self.repetitions = 1

settings = Settings()
