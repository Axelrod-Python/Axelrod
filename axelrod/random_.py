import random

import numpy as np
from numpy.random import choice

from axelrod.action import Action

C, D = Action.C, Action.D


def seed(seed_):
    """Sets a seed"""
    random.seed(seed_)
    np.random.seed(seed_)


def random_choice(p: float = 0.5) -> Action:
    """
    Return C with probability `p`, else return D

    No random sample is carried out if p is 0 or 1.

    Parameters
    ----------
    p : float
        The probability of picking C

    Returns
    -------
    axelrod.Action
    """
    if p == 0:
        return D

    if p == 1:
        return C

    r = random.random()
    if r < p:
        return C
    return D


def random_flip(action: Action, threshold: float) -> Action:
    """
    Return flipped action with probability `threshold`

    No random sample is carried out if threshold is 0 or 1.

    Parameters
    ----------
    action:
        The action to flip or not
    threshold : float
        The probability of flipping action

    Returns
    -------
    axelrod.Action
    """
    if random_choice(threshold) == C:
        return action.flip()
    return action


def randrange(a: int, b: int) -> int:
    """Python 2 / 3 compatible randrange. Returns a random integer uniformly
    between a and b (inclusive)"""
    c = b - a
    r = c * random.random()
    return a + int(r)


def random_vector(size):
    """Create a random vector of values in [0, 1] that sums to 1."""
    vector = []
    s = 1
    for _ in range(size - 1):
        r = s * random.random()
        vector.append(r)
        s -= r
    vector.append(s)
    return vector


class Pdf(object):
    """A class for a probability distribution"""

    def __init__(self, counter):
        """Take as an instance of collections.counter"""
        self.sample_space, self.counts = zip(*counter.items())
        self.size = len(self.sample_space)
        self.total = sum(self.counts)
        self.probability = list([v / self.total for v in self.counts])

    def sample(self):
        """Sample from the pdf"""
        index = choice(a=range(self.size), p=self.probability)
        # Numpy cannot sample from a list of n dimensional objects for n > 1,
        # need to sample an index.
        return self.sample_space[index]
