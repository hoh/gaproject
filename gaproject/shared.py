'''
Empty module used to store global objects within GAPROJECT.
'''

import sys


class Settings(object):

    def __init__(self):
        self.plot = 'plot' in sys.argv

settings = Settings()
