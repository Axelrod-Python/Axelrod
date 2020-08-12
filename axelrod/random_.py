from typing import Optional

import numpy as np
from axelrod.action import Action
from numpy.random import RandomState

C, D = Action.C, Action.D


class RandomGenerator(object):
    """Container around a random number generator.
    Enables reproducibility of player behavior, matches,
    and tournaments."""
    def __init__(self, seed: Optional[int] = None):
        # _random is the internal object that generators random values
        self._random = RandomState()
        self.original_seed = seed
        self.seed(seed)

    def seed(self, seed_: Optional[int] = None):
        """Sets a seed"""
        self._random.seed(seed_)

    def random(self, *args, **kwargs):
        return self._random.rand(*args, **kwargs)

    def randint(self, *args, **kwargs):
        return self._random.randint(*args, **kwargs)

    def random_seed_int(self) -> int:
        return self.randint(low=0, high=2**32-1, dtype="uint64")

    def choice(self, *args, **kwargs):
        return self._random.choice(*args, **kwargs)

    def uniform(self, *args, **kwargs):
        return self._random.uniform(*args, **kwargs)

    def random_choice(self, p: float = 0.5) -> Action:
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

        r = self.random()
        if r < p:
            return C
        return D

    def random_flip(self, action: Action, threshold: float) -> Action:
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
        if self.random_choice(threshold) == C:
            return action.flip()
        return action

    def randrange(self, a: int, b: int) -> int:
        """Returns a random integer uniformly between a and b: [a, b)."""
        c = b - a
        r = c * self.random()
        return a + int(r)

    def random_vector(self, size):
        """Create a random vector of values in [0, 1] that sums to 1."""
        vector = self.random(size)
        return np.array(vector) / np.sum(vector)


class Pdf(object):
    """A class for a probability distribution"""

    def __init__(self, counter, seed=None):
        """Take as an instance of collections.counter"""
        self.sample_space, self.counts = zip(*counter.items())
        self.size = len(self.sample_space)
        self.total = sum(self.counts)
        self.probability = list([v / self.total for v in self.counts])
        self._random = RandomGenerator(seed=seed)

    def sample(self):
        """Sample from the pdf"""
        index = self._random.choice(a=range(self.size), p=self.probability)
        # Numpy cannot sample from a list of n dimensional objects for n > 1,
        # need to sample an index.
        return self.sample_space[index]


class BulkRandomGenerator(object):
    """Bulk generator of random integers for tournament seeding and
    reproducibility. Bulk generation of random values is more efficient.
    Use this class like a generator."""
    def __init__(self, seed=None, batch_size:int = 1000):
        self._random_generator = RandomState()
        self._random_generator.seed(seed)
        self._ints = None
        self._batch_size = batch_size
        self._index = 0
        self._fill_ints()

    def _fill_ints(self):
        # Generate more random values. Store as a list since generators
        # cannot be pickled.
        self._ints = self._random_generator.randint(
            low=0,
            high=2**32 - 1,
            size=self._batch_size,
            dtype="uint64")
        self._index = 0

    def __next__(self):
        try:
            x = self._ints[self._index]
        except IndexError:
            self._fill_ints()
            x = self._ints[self._index]
        self._index += 1
        return x
