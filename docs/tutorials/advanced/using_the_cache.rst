.. _using-the-cache:

Using the cache
===============

Whilst for stochastic strategies, every repetition of a Match will give a
different result, for deterministic strategies, when there is no noise there is
no need to re run the match. The library has a :code:`DeterministicCache` class
that allows us to quickly replay matches.

Here is how to create a new empty cache::

    >>> import axelrod as axl
    >>> cache = axl.DeterministicCache()
    >>> len(cache)
    0

Caching a Match
---------------

We can use this cache in a Match, let us also time the execution::

    >>> import timeit
    >>> def run_match():
    ...     p1, p2 = axl.GoByMajority(), axl.Alternator()
    ...     match = axl.Match((p1, p2), deterministic_cache=cache, turns=200)
    ...     return match.play()
    >>> time_with_empty_cache = timeit.timeit(run_match, number=500)

We can take a look at the cache::

    >>> cache  # doctest: +ELLIPSIS
    {(<class 'axelrod.strategies.gobymajority.GoByMajority'>, <class 'axelrod.strategies.alternator.Alternator'>, 200): [('C', 'C'), ..., ('C', 'D')]}
    >>> len(cache)
    1

This maps a triplet of 2 player classes and the match length to the resulting
interactions.  We can rerun the code and compare the timing::

    >>> time_with_full_cache = timeit.timeit(run_match, number=200)
    >>> time_with_empty_cache  # doctest: +SKIP
    0.039147138595581055
    >>> time_with_full_cache  # doctest: +SKIP
    0.014961004257202148
    >>> time_with_full_cache < time_with_empty_cache
    True

Note that we can write the cache to file::

    >>> cache.save("cache.txt")
    True

Caching a Tournament
--------------------

We can use a prebuilt cache in a tournament (by default a new cache is used). Firstly,
let us read in the previous cache from file::

    >>> cache = axl.DeterministicCache("cache.txt")
    >>> cache  # doctest: +ELLIPSIS
    {(<class 'axelrod.strategies.gobymajority.GoByMajority'>, <class 'axelrod.strategies.alternator.Alternator'>, 200): [('C', 'C'), ...]}

Let us create a tournament including :code:`GoByMajority` and :code:`Alternator`
to be able to make use of the cache::

    >>> players = [axl.GoByMajority(), axl.Alternator(), axl.Cooperator()]
    >>> tournament = axl.Tournament(players, turns=200, repetitions=5, deterministic_cache=cache)
    >>> results = tournament.play()

The cache has not only been used for this but has now also been updated with the
new matches::

    >>> len(cache)
    6

Caching a Moran Process
-----------------------

A prebuilt cache can also be used in a Moran process (by default a new cache is
used)::

    >>> players = [axl.GoByMajority(), axl.Alternator(),
    ...            axl.Cooperator(), axl.Grudger()]
    >>> mp = axl.MoranProcess(players, deterministic_cache=cache)
    >>> populations = mp.play()
    >>> mp.winning_strategy_name   # doctest: +SKIP
    Defector

Again we see that the cache has been augmented, although note that this
particular number will depend on the stochastic behaviour of the Moran process::

    >>> len(cache)  # doctest: +SKIP
    18

Although, in this case the length of matches are not all the same (the default
match length in the Moran process is 100)::

    >>> list(set([length for p1, p2, length in cache.keys()]))
    [200, 100]
