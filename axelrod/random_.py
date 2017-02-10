import random
import numpy
from axelrod.actions import Action, Actions


def random_choice(p: float = 0.5) -> Action:
    """
    Return 'C' with probability `p`, else return 'D'

    No random sample is carried out if p is 0 or 1.

    Parameters
    ----------

    p : float
        The probability of picking 'C'

    Returns
    -------
    axelrod.Actions.C or axelrod.Actions.D
    """
    if p == 0:
        return Actions.D

    if p == 1:
        return Actions.C

    r = random.random()
    if r < p:
        return Actions.C
    return Actions.D


def randrange(a: int, b: int) -> int:
    """Python 2 / 3 compatible randrange. Returns a random integer uniformly
    between a and b (inclusive)"""
    c = b - a
    r = c * random.random()
    return a + int(r)


def seed(seed_):
    """Sets a seed"""
    random.seed(seed_)
    numpy.random.seed(seed_)
