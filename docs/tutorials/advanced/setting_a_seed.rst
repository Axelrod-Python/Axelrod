.. _setting_a_seed:

Setting a random seed
=====================

The library has a variety of strategies whose behaviour is stochastic. To ensure
reproducible results a random seed should be set. As both Numpy and the standard
library are used for random number generation, both seeds need to be
set. To do this we can use the `set_seed` function::

    >>> import axelrod as axl
    >>> players = (axl.Random(), axl.MetaMixer())  # Two stochastic strategies
    >>> axl.set_seed(0)
    >>> axl.Match(players, turns=3).play()
    [('D', 'C'), ('D', 'D'), ('C', 'D')]

We obtain the same results is it is played with the same seed::

    >>> axl.set_seed(0)
    >>> axl.Match(players, turns=3).play()
    [('D', 'C'), ('D', 'D'), ('C', 'D')]

Note that this is equivalent to::

    >>> import numpy
    >>> import random
    >>> players = (axl.Random(), axl.MetaMixer())
    >>> random.seed(0)
    >>> numpy.random.seed(0)
    >>> axl.Match(players, turns=3).play()
    [('D', 'C'), ('D', 'D'), ('C', 'D')]
    >>> numpy.random.seed(0)
    >>> random.seed(0)
    >>> axl.Match(players, turns=3).play()
    [('D', 'C'), ('D', 'D'), ('C', 'D')]
