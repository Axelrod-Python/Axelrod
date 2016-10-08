.. _setting_a_seed:

Setting a random seed
=====================

The library has a variety of strategies whose behaviour is stochastic. To ensure
reproducible results a random seed should be set. As both Numpy and the standard
library are used for random number generation, both seeds need to be
set. To do this we can use the `seed` function::

    >>> import axelrod as axl
    >>> players = (axl.Random(), axl.MetaMixer())  # Two stochastic strategies
    >>> axl.seed(0)
    >>> results = axl.Match(players, turns=3).play()

We obtain the same results if it is played with the same seed::

    >>> axl.seed(0)
    >>> results == axl.Match(players, turns=3).play()
    True

Note that this is equivalent to::

    >>> import numpy
    >>> import random
    >>> players = (axl.Random(), axl.MetaMixer())
    >>> random.seed(0)
    >>> numpy.random.seed(0)
    >>> results = axl.Match(players, turns=3).play()
    >>> numpy.random.seed(0)
    >>> random.seed(0)
    >>> results == axl.Match(players, turns=3).play()
    True
