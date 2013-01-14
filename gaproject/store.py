
'''
The store aims at storing results in a MongoDB database and
retrieving them.

Uses PyMongo, see doc on:
    http://api.mongodb.org/python/current/tutorial.html

'''

import sys
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient


def Store():
    try:
        connection = MongoClient('localhost')
        return connection['gaproject']
    except ConnectionFailure:
        print 'Error: could not connect to DB'
        sys.exit()
