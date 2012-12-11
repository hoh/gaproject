'''
Empty module used to store global objects within GAPROJECT.
'''

import sys


class Settings(object):

    def __init__(self):
        self.plot = 'plot' in sys.argv
        self.generations = 100
        self.population = 300
        self.loop_removal = True

settings = Settings()
