.. _using-the-cache:

Using the cache
===============

Whilst for stochastic strategies, every repetition of a Match will give a
different result, for deterministic strategies, when there is no noise there is
no need to re run the match. The library has a :code:`DeterministicCache` class
that allows us to quickly replay matches.


Caching a Match
---------------

To illustrate this, let us time the play of a match **without** a cache::

    >>> import axelrod as axl
    >>> import timeit
    >>> def run_match():
    ...     p1, p2 = axl.GoByMajority(), axl.Alternator()
    ...     match = axl.Match((p1, p2), turns=200)
    ...     return match.play()
    >>> time_with_no_cache = timeit.timeit(run_match, number=500)
    >>> time_with_no_cache  # doctest: +SKIP
    2.2295279502868652

Here is how to create a new empty cache::

    >>> cache = axl.DeterministicCache()
    >>> len(cache)
    0

Let us rerun the above match but using the cache::

    >>> p1, p2 = axl.GoByMajority(), axl.Alternator()
    >>> match = axl.Match((p1, p2), turns=200, deterministic_cache=cache)
    >>> match.play()  # doctest: +ELLIPSIS
    [('C', 'C'), ..., ('C', 'D')]

We can take a look at the cache::

    >>> cache  # doctest: +ELLIPSIS
    {(<class 'axelrod.strategies.gobymajority.GoByMajority'>, <class 'axelrod.strategies.alternator.Alternator'>, 200): [('C', 'C'), ..., ('C', 'D')]}
    >>> len(cache)
    1

This maps a triplet of 2 player classes and the match length to the resulting
interactions.  We can rerun the code and compare the timing::

    >>> def run_match_with_cache():
    ...     p1, p2 = axl.GoByMajority(), axl.Alternator()
    ...     match = axl.Match((p1, p2), turns=200, deterministic_cache=cache)
    ...     return match.play()
    >>> time_with_cache = timeit.timeit(run_match_with_cache, number=500)
    >>> time_with_cache  # doctest: +SKIP
    0.04215192794799805
    >>> time_with_cache < time_with_no_cache
    True

We can write the cache to file::

    >>> cache.save("cache.txt")
    True

Caching a Tournament
--------------------

Tournaments will automatically create caches as needed on a match by match
basis.

Caching a Moran Process
-----------------------

A prebuilt cache can also be used in a Moran process (by default a new cache is
used)::

    >>> cache = axl.DeterministicCache("cache.txt")
    >>> players = [axl.GoByMajority(), axl.Alternator(),
    ...            axl.Cooperator(), axl.Grudger()]
    >>> mp = axl.MoranProcess(players, deterministic_cache=cache)
    >>> populations = mp.play()
    >>> mp.winning_strategy_name   # doctest: +SKIP
    Defector

We see that the cache has been augmented, although note that this
particular number will depend on the stochastic behaviour of the Moran process::

    >>> len(cache)  # doctest: +SKIP
    18

Although, in this case the length of matches are not all the same (the default
match length in the Moran process is 100)::

    >>> list(set([length for p1, p2, length in cache.keys()]))
    [200, 100]
