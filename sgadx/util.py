"""Random Utilities

Function from this class are generic enough that I don't know where else to put them

"""

import random
from numpy.linalg import norm

def flip(bias=0.5):
    """

    """

    return random.random() < bias

def unit_vector_average(*unit_vectors):
    """
    if there's one function to optimize (e.g. Cython) it's this one
    """

    v = sum(unit_vectors)

    return (v)/norm(v)