'''
Empty module used to store global objects within GAPROJECT.
'''

import sys


class Settings(object):
    'Shared object containing all global settings.'

    def __init__(self):
        self.plot = 'plot' in sys.argv
        self.loop_removal = True
        # Number of populations for MetaGA, use False or 1 to disable:
        self.metaGA = 4

    def __getitem__(self, name):
        'Allows Settings to be used as a dictionary as well.'
        return self.__getattribute__(name)

settings = Settings()

# The following will be replaced by the real value in run.py:
data = None
orderedSequenceOfNodes = None
