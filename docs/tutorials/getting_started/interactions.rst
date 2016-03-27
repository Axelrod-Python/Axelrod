Accessing the interactions
==========================

This tutorial will show you briefly how to access the detailed interaction
results corresponding to the tournament.

To access the detailed interaction results we create a tournament as usual
(see :ref:`getting-started`)::

    >>> import axelrod as axl
    >>> strategies = [
    ...     axl.Cooperator(), axl.Defector(),
    ...     axl.TitForTat(), axl.Grudger()]
    >>> tournament = axl.Tournament(strategies, turns=3, repetitions=1)
    >>> results = tournament.play()

The tournament object has a 'matches' attribute which is a list of axelrod.Match
objects. (Actually, it's a list of lists: one list for each repetition which, in
turn, has a list of Match objects). Each match object holds the pair of
axelrod.Player objects for that match and the history of their interactions::

    >>> for match in tournament.matches[0]:
    ...     player1 = match.player1.name
    ...     player2 = match.player2.name
    ...     print('%s vs %s: %s' % (player1, player2, match.result)) # doctest: +SKIP
    Cooperator vs Defector: [('C', 'D'), ('C', 'D'), ('C', 'D')]
    Defector vs Tit For Tat: [('D', 'C'), ('D', 'D'), ('D', 'D')]
    Cooperator vs Cooperator: [('C', 'C'), ('C', 'C'), ('C', 'C')]
    Tit For Tat vs Grudger: [('C', 'C'), ('C', 'C'), ('C', 'C')]
    Grudger vs Grudger: [('C', 'C'), ('C', 'C'), ('C', 'C')]
    Tit For Tat vs Tit For Tat: [('C', 'C'), ('C', 'C'), ('C', 'C')]
    Defector vs Grudger: [('D', 'C'), ('D', 'D'), ('D', 'D')]
    Cooperator vs Grudger: [('C', 'C'), ('C', 'C'), ('C', 'C')]
    Cooperator vs Tit For Tat: [('C', 'C'), ('C', 'C'), ('C', 'C')]
    Defector vs Defector: [('D', 'D'), ('D', 'D'), ('D', 'D')]

There is further detail on axelrod.Match objects and the information you can
retrieve from them in :ref:`creating_matches`.
