Using and playing different stage games
=======================================

As described in :ref:`play_contexts` the default game used for the Prisoner's
Dilemma is given by::

    >>> import axelrod as axl
    >>> pd = axl.game.Game()
    >>> pd
    Axelrod game: (R,P,S,T) = (3, 1, 0, 5)
    >>> pd.RPST()
    (3, 1, 0, 5)

These :code:`Game` objects are used to score :ref:`matches <creating_matches>`,
:ref:`tournaments <making_tournaments>` and :ref:`Moran processes
<moran-process>`::

    >>> pd.score((axl.Actions.C, axl.Actions.C))
    (3, 3)
    >>> pd.score((axl.Actions.C, axl.Actions.D))
    (0, 5)
    >>> pd.score((axl.Actions.D, axl.Actions.C))
    (5, 0)
    >>> pd.score((axl.Actions.D, axl.Actions.D))
    (1, 1)

It is possible to run a matches, tournaments and Moran processes with a
different game. For example here is the game of chicken::

    >>> chicken = axl.game.Game(r=0, s=-1, t=1, p=-10)
    >>> chicken
    Axelrod game: (R,P,S,T) = (0, -10, -1, 1)
    >>> chicken.RPST()
    (0, -10, -1, 1)

Here is a simple tournament run with this game::

    >>> players = [axl.Cooperator(), axl.Defector(), axl.TitForTat()]
    >>> tournament = axl.Tournament(players, game=chicken)
    >>> results = tournament.play()
    >>> results.ranked_names
    ['Cooperator', 'Defector', 'Tit For Tat']

The default Prisoner's dilemma has different results::

    >>> tournament = axl.Tournament(players)
    >>> results = tournament.play()
    >>> results.ranked_names
    ['Defector', 'Tit For Tat', 'Cooperator']
