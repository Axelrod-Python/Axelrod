.. _approximate-moran-process:

Approximate Moran Process
=========================

Due to the high computational cost of a single Moran process, an approximate
Moran process is implemented that can make use of cached outcomes of games. The
following code snippet will generate a Moran process in which the outcomes of
the matches played by a :code:`Random: 0.5` are sampled from one possible
outcome against each opponent (:code:`Defector` and :code:`Random: 0.5`). First
the cache is built by passing counter objects of outcomes::

    >>> import axelrod as axl
    >>> from collections import Counter
    >>> cached_outcomes = {}
    >>> cached_outcomes[("Random: 0.5", "Defector")] = axl.Pdf(Counter([(1, 1)]))
    >>> cached_outcomes[("Random: 0.5", "Random: 0.5")] = axl.Pdf(Counter([(3, 3)]))
    >>> cached_outcomes[("Defector", "Defector")] = axl.Pdf(Counter([(1, 1)]))

Now let us create an Approximate Moran Process::

    >>> players = [axl.Defector(), axl.Random(), axl.Random()]
    >>> amp = axl.ApproximateMoranProcess(players, cached_outcomes, seed=5)
    >>> results = amp.play()
    >>> amp.population_distribution()
    Counter({'Random: 0.5': 3})

Note that by nature of being an approximation, it's possible that the results of an
`ApproximateMoranProcess` may not always match the results of a standard `MoranProcess`,
even for the same random seed. We see that, for this random seed, the :code:`Random: 0.5`
won this Moran process. This is not what happens in a standard Moran process where the
:code:`Random: 0.5` player will not win::

    >>> mp = axl.MoranProcess(players, seed=5)
    >>> results = mp.play()
    >>> mp.population_distribution()
    Counter({'Defector': 3})
