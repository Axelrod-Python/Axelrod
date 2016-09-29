.. _human-interaction:

Human Interaction
=================

It is possible to play interactively using the Human strategy::

    >>> import axelrod as axl
    >>> me = axl.Human(name='me')
    >>> players = [axl.TitForTat(), me]
    >>> match = axl.Match(players, turns=3)
    >>> match.play() #doctest: +SKIP

You will be prompted for the action to play at each turn and will be able to
access the results of the match as described in :ref:`creating_matches`
