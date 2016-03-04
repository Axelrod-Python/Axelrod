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
    ...     strategies, turns=3, repetitions=1, keep_matches=True)
    >>> results = tournament.play()

The detailed interactions are now available to us. The tournament object has
a 'matches' attribute which is a list of axelrod.Match objects. (Actually, it's
a list of lists: one list for each repetition which, in turn, has a list of
Match objects). Each match object holds the pair of axelrod.Player objects for
that match and the history of their interactions::

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
