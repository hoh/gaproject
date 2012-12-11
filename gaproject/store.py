
'''
The store aims at storing results in a MongoDB database and
retrieving them.

Uses PyMongo, see doc on:
    http://api.mongodb.org/python/current/tutorial.html

'''

from pymongo import MongoClient


def Store():
    connection = MongoClient()
    return connection['gaproject']
