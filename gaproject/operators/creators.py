
import random
import gaproject.shared as shared


def path_creator():
    'Creates a path individual'
    ind_size = len(shared.data)
    return random.sample(xrange(ind_size), ind_size)
