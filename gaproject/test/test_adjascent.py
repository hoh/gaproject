
import pytest

# Loading data:
from gaproject.data import Box
import gaproject.shared as shared
box = Box('data/TSPBenchmark')
shared.data = box.get('belgiumtour.tsp')

import gaproject.operators.creators as creators
from gaproject.operators.evaluators import fromPathToAdjacent, fromAdjacentToPath


def test_fromPathToAdjacent():
    path_individual = creators.path_creator()
    print path_individual
    adj_individual = fromPathToAdjacent(path_individual)
    print adj_individual


def test_fromAdjacentToPath():
    adj_individual = creators.adj_creator()
    path_individual = fromAdjacentToPath(adj_individual)
    print path_individual


def test_loopConversion():
    'Testing if we get the same result after the two translations:'
    orig = creators.path_creator()
    adj_individual = fromPathToAdjacent(orig)
    new = fromAdjacentToPath(adj_individual)

    index = orig.index(0)
    o = orig[index:] + orig[0:index]
    assert o == list(new)


def test_creator():
    individual = creators.adj_creator()
    assert individual is not None
