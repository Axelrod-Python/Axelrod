.. _player_information:

Player information
==================

It is possible to determine what information players know about their matches.
By default all known information is given.
For example let us create a match with 5 turns between :code:`SteinAndRapoport`
and :code:`Alternator`. The latter of these two always defects on the last 2
turns::

    >>> import axelrod as axl
    >>> players = (axl.Alternator(), axl.SteinAndRapoport())
    >>> axl.Match(players, turns=5).play()
    [(C, C), (D, C), (C, C), (D, D), (C, D)]

We can play the same match but let us tell the players that the match lasts 6
turns::

    >>> axl.Match(players, turns=5, match_attributes={"length": 6}).play()
    [(C, C), (D, C), (C, C), (D, C), (C, D)]

We can also pass this information to a tournament. Let us create a
tournament with 5 turns but ensure the players believe the match length is
infinite (unknown)::

    >>> tournament = axl.Tournament(players, turns=5,
    ...                             match_attributes={"length": float('inf')})

The :code:`match_attributes` dictionary can also be used to pass :code:`game`
and :code:`noise`.
