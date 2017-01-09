import random
import numpy
from axelrod import Actions

C, D = Actions.C, Actions.D

def random_choice(p=0.5):
    """
    Return 'C' with probability `p`, else return 'D'

    Emulates Python's random.choice(['C', 'D']) since it is not consistent
    across Python 2.7 to Python 3.4

    Parameters
    ----------

    p : float
        The probability of picking 'C'

    Returns
    -------
    axelrod.Actions.C or axelrod.Actions.D
    """
    assert (p >= 0) and (p <= 1)
    if p == 0:
        return D

    if p == 1:
        return C

    r = random.random()
    if r < p:
        return C
    return D


def randrange(a, b):
    """Python 2 / 3 compatible randrange. Returns a random integer uniformly
    between a and b (inclusive)"""
    c = b - a
    r = c * random.random()
    return a + int(r)


def seed(seed_):
    """Sets a seed"""
    random.seed(seed_)
    numpy.random.seed(seed_)
