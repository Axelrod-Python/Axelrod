import random
import numpy
from axelrod import Actions


choices = {
    0: Actions.D,
    1: Actions.C
}


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

    if p in [0, 1]:
        choice = choices[p]
    else:
        r = random.random()
        choice = choices[r < p]

    return choice


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
