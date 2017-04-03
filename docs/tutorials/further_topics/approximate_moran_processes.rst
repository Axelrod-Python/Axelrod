.. _approximate-moran-process:

Approximate Moran Process
=========================

Due to the high computational cost of a single Moran process, an approximate
Moran process is implemented that can make use of cached outcomes of games. The
following code snippet will generate a Moran process in which a `Defector`
cooperates (gets a high score) against another `Defector`. First the cache is
built by passing counter objects of outcomes::

    >>> import axelrod as axl
    >>> from collections import Counter
    >>> cached_outcomes = {}
    >>> cached_outcomes[("Cooperator", "Defector")] = axl.Pdf(Counter([(0, 5)]))
    >>> cached_outcomes[("Cooperator", "Cooperator")] = axl.Pdf(Counter([(3, 3)]))
    >>> cached_outcomes[("Defector", "Defector")] = axl.Pdf(Counter([(10, 10), (9, 9)]))

Now let us create an Approximate Moran Process::

    >>> axl.seed(0)
    >>> players = [axl.Cooperator(), axl.Defector(), axl.Defector(), axl.Defector()]
    >>> amp = axl.ApproximateMoranProcess(players, cached_outcomes)
    >>> results = amp.play()
    >>> amp.population_distribution()
    Counter({'Defector': 4})
