'''
Empty module used to store global objects within GAPROJECT.
'''

import sys


class Settings(object):

    def __init__(self):
        self.plot = 'plot' in sys.argv
        self.generations = 50
        self.population = 100
        self.loop_removal = True
        self.repetitions = 2

settings = Settings()
