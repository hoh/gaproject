'''
Empty module used to store global objects within GAPROJECT.
'''

import sys


class Settings(object):

    def __init__(self):
        self.plot = 'plot' in sys.argv
        self.generations = 101
        self.population = 101
        self.loop_removal = True
        self.repetitions = 2

    def __getitem__(self, name):
        return self.__getattribute__(name)

    def fallback(self, dico, key):
        'Returns dico[key] or fallbacks to self.key.'
        return dico.get(key, settings[key])

settings = Settings()

# The following will be replaced by the real value in run.py:
data = None
orderedSequenceOfNodes = None
