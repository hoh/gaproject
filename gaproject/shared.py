'''
Empty module used to store global objects within GAPROJECT.
'''

import sys
import os


class Settings(object):
    'Shared object containing all global settings.'

    def __init__(self):
        self.plot = 'plot' in sys.argv
        self.loop_removal = True
        # Number of populations for MetaGA, use False or 1 to disable:
        self.metaGA = 4
        if os.uname()[1] == 'okso.local':
            self.filesDir = os.path.expanduser('/tmp/lithium/GAP_results')
        else:
            self.filesDir = os.path.expanduser('~/GAP_results')

        if not os.path.isdir(self.filesDir):
            os.mkdir(self.filesDir)

    def __getitem__(self, name):
        'Allows Settings to be used as a dictionary as well.'
        return self.__getattribute__(name)

settings = Settings()


# The following will be replaced by the real value in run.py:
data = None
orderedSequenceOfNodes = None
