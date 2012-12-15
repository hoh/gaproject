
import random
import gaproject.shared as shared
from gaproject.operators.evaluators import fromPathToAdjacent

def path_creator():
    'Creates a path individual'
    ind_size = len(shared.data)
    return random.sample(xrange(ind_size), ind_size)

def adj_creator():

    'Creates a valid adjacent individual'
    return fromPathToAdjacent(path_creator())
