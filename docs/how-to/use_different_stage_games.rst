.. _use_different_stage_games:

Use different stage games
=========================

As described in :ref:`play_contexts` the default game used for the Prisoner's
Dilemma is given by::

    >>> import axelrod as axl
    >>> pd = axl.game.Game()
    >>> pd
    Axelrod game: (R,P,S,T) = (3, 1, 0, 5)
    >>> pd.RPST()
    (3, 1, 0, 5)

These :code:`Game` objects are used to score :ref:`matches <creating_matches>`,
:ref:`tournaments <creating_tournaments>` and :ref:`Moran processes
<moran-process>`::

    >>> pd.score((axl.Action.C, axl.Action.C))
    (3, 3)
    >>> pd.score((axl.Action.C, axl.Action.D))
    (0, 5)
    >>> pd.score((axl.Action.D, axl.Action.C))
    (5, 0)
    >>> pd.score((axl.Action.D, axl.Action.D))
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

Asymmetric games can also be implemented via the AsymmetricGame class 
with two Numpy arrays for payoff matrices::

    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 3]])
    >>> B = np.array([[1, 3], [2, 1]])
    >>> asymmetric_game = axl.AsymmetricGame(A, B)
    >>> asymmetric_game  # doctest: +NORMALIZE_WHITESPACE
    Axelrod game with matrices: (array([[3, 1],
                                        [1, 3]]),
                                 array([[1, 3],
                                        [2, 1]]))

Asymmetric games can also be different sizes (even if symmetric; regular games
can currently only be 2x2), such as Rock Paper Scissors::

    >>> A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    >>> rock_paper_scissors = axl.AsymmetricGame(A, -A)
    >>> rock_paper_scissors  # doctest: +NORMALIZE_WHITESPACE
    Axelrod game with matrices: (array([[ 0, -1,  1],
                                        [ 1,  0, -1],
                                        [-1,  1,  0]]),
                                 array([[ 0,  1, -1],
                                        [-1,  0,  1],
                                        [ 1, -1,  0]]))

**NB: Some features of Axelrod, such as strategy transformers, are specifically created for
use with the iterated Prisoner's Dilemma; they may break with games of other sizes.**
Note also that most strategies in Axelrod are Prisoners' Dilemma strategies, so behave
as though they are playing the Prisoners' Dilemma; in the rock-paper-scissors example above,
they will certainly never choose scissors (because their strategy action set is two actions!)

For a more detailed tutorial on how to implement another game into Axelrod, :ref:`here is a 
tutorial using rock paper scissors as an example. <implement-new-games>`