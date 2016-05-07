Accessing the interactions
==========================

This tutorial will show you briefly how to access the detailed interaction
results corresponding to the tournament.

To access the detailed interaction results we create a tournament as usual
(see :ref:`creating_tournaments`)::

    >>> import axelrod as axl
    >>> players = [
    ...     axl.Cooperator(), axl.Defector(),
    ...     axl.TitForTat(), axl.Grudger()]
    >>> tournament = axl.Tournament(players, turns=3, repetitions=1)
    >>> results = tournament.play()

The tournament object has an 'interactions' attribute which contains all the
interactions between the players.
(Actually, it's a list of lists: one list for each repetition which, in
turn, has a list of Match objects). These can be used to view the history of the
interactions::

    >>> for index_pair, interaction in results.interactions.items():
    ...     player1 = tournament.players[index_pair[0]]
    ...     player2 = tournament.players[index_pair[1]]
    ...     print('%s vs %s: %s' % (player1, player2, interaction)) # doctest: +SKIP
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

We can use these interactions to reconstruct :code:`axelrod.Match` objects which have
a variety of available methods for analysis (more information can be found in
:ref:`creating_matches`)::

    >>> matches = []
    >>> for index_pair, interaction in results.interactions.items():
    ...     player1 = tournament.players[index_pair[0]]
    ...     player2 = tournament.players[index_pair[1]]
    ...     match = axl.Match([player1, player2], turns=3)
    ...     match.result = interaction
    ...     matches.append(match)
    >>> len(matches)
    10

As an example let us view all winners of each match (:code:`False` indicates a
tie):

    >>> for match in matches:
    ...     print("{} v {}, winner: {}".format(match.players[0], match.players[1], match.winner()))  #doctest: +SKIP
	Cooperator v Defector, winner: Defector
    Defector v Tit For Tat, winner: Defector
    Cooperator v Cooperator, winner: False
    Tit For Tat v Grudger, winner: False
    Grudger v Grudger, winner: False
    Tit For Tat v Tit For Tat, winner: False
    Defector v Grudger, winner: Defector
    Cooperator v Grudger, winner: False
    Cooperator v Tit For Tat, winner: False
    Defector v Defector, winner: False

