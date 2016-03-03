Accessing the interactions
==========================

This tutorial will show you briefly how to access the detailed interaction
results corresponding to the tournament.

As shown in :ref:`getting-started` let us create a tournament except that,
this time, we will set the with_interactions parameter. (We will also reduce
the number of turns per match to 3 and we'll run only a single repetition)::

    >>> import axelrod as axl
    >>> strategies = [
    ...     axl.Cooperator(), axl.Defector(),
    ...     axl.TitForTat(), axl.Grudger()]
    >>> tournament = axl.Tournament(
    ...     strategies, turns=3, repetitions=1, with_interactions=True)
    >>> tournament.play()

We can now view the detailed interactions that occurred between the players
for each turn in each match. (The interactions are stored within a dictionary,
so we'll add a sort to show the entries in a sensible order).::

    >>> for key in sorted(tournament.interactions):
    ...     print('%s: %s' % (key, tournament.interactions[key]))
    (0, 0): [('C', 'C'), ('C', 'C'), ('C', 'C')]
    (0, 1): [('C', 'D'), ('C', 'D'), ('C', 'D')]
    (0, 2): [('C', 'C'), ('C', 'C'), ('C', 'C')]
    (0, 3): [('C', 'C'), ('C', 'C'), ('C', 'C')]
    (1, 1): [('D', 'D'), ('D', 'D'), ('D', 'D')]
    (1, 2): [('D', 'C'), ('D', 'D'), ('D', 'D')]
    (1, 3): [('D', 'C'), ('D', 'D'), ('D', 'D')]
    (2, 2): [('C', 'C'), ('C', 'C'), ('C', 'C')]
    (2, 3): [('C', 'C'), ('C', 'C'), ('C', 'C')]
    (3, 3): [('C', 'C'), ('C', 'C'), ('C', 'C')]
