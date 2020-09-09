.. _setting_a_seed:

Setting a random seed
=====================

The library has a variety of strategies whose behaviour is stochastic. To ensure
reproducible results a random seed should be set. The library abstracts away the
propagation of seeds in matches and tournaments, so you typically only need to
supply a seed to those objects.

Matches
-------

For a match, set a seed by passing a parameter to `Match`

    >>> import axelrod as axl
    >>> players = (axl.Random(), axl.MetaMixer())  # Two stochastic strategies
    >>> match = axl.Match(players, turns=3, seed=101)
    >>> results = match.play()

We obtain the same results if it is played with the same seed::

    >>> match2 = axl.Match(players, turns=3, seed=101)
    >>> result2 = match2.play()
    >>> results == result2
    True

For noisy matches, a seed also needs to be set for reproducibility, even if the players are
deterministic.

    >>> import axelrod as axl
    >>> players = (axl.Cooperator(), axl.Defector())  # Two deterministic strategies
    >>> match = axl.Match(players, turns=200, seed=101, noise=0.25)
    >>> results = match.play()
    >>> match2 = axl.Match(players, turns=200, seed=101, noise=0.25)
    >>> results2 = match2.play()
    >>> results == results2
    True

Tournaments
-----------

For tournaments, an initial seed is used to generate subsequent seeds for each match in a
a manner that will yield identical results. Note that if the tournament is run with multiple
processes, the order of the matches may be computed differently, but the seeds used for each
match will be the same.

To seed a tournament we also pass a seed to the tournament at creation time:

    >>> import axelrod as axl
    >>> seed = 201
    >>> players = (axl.Random(), axl.Cooperator(), axl.MetaMixer())
    >>> tournament = axl.Tournament(players, turns=5, repetitions=5, seed=seed)
    >>> results = tournament.play(processes=1)
    >>> tournament2 = axl.Tournament(players, turns=5, repetitions=5, seed=seed)
    >>> results2 = tournament2.play(processes=1)
    >>> results.ranked_names == results2.ranked_names
    True

For parallel processing, the ordering of match results may differ, but the actual results, and the final
rankings, will be the same.

    >>> import axelrod as axl
    >>> players = (axl.Random(), axl.Cooperator(), axl.MetaMixer())
    >>> tournament = axl.Tournament(players, turns=5, repetitions=5, seed=201)
    >>> results = tournament.play(processes=2)
    >>> tournament2 = axl.Tournament(players, turns=5, repetitions=5, seed=201)
    >>> results2 = tournament2.play(processes=2)
    >>> results.ranked_names == results2.ranked_names
    True


Moran Process
-------------

Similarly, a Moran process is essentially another type of tournament. The library's implementation
will propagate child seeds to each match to ensure reproducibility. See also the documentation on
:code:`EvolvablePlayers`.


Fingerprints
------------
Since fingerprint generation depends on tournaments, fingerprints can also be given a seed for
reproducibility.
