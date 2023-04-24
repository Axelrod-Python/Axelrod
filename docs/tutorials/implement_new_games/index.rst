.. _implement-new-games:
.. highlight:: python

Implement new games
===================

Currently, the default :code:`Strategy`, :code:`Action` and :code:`Game` 
implementations in Axelrod are centred around the Iterated Prisoners' Dilemma. 
The stage game can be changed as shown in :ref:`use_different_stage_games`.

However, just changing the stage game may not be sufficient. Take, for example, the
game rock-paper-scissors::

    >>> import axelrod as axl
    >>> import numpy as np
    >>> A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    >>> rock_paper_scissors = axl.AsymmetricGame(A, -A)
    >>> rock_paper_scissors  # doctest: +NORMALIZE_WHITESPACE
    Axelrod game with matrices: (array([[ 0, -1,  1],
                                        [ 1,  0, -1],
                                        [-1,  1,  0]]),
                                 array([[ 0,  1, -1],
                                        [-1,  0,  1],
                                        [ 1, -1,  0]]))

If we tried to run a rock-paper-scissors match with the :code:`Tit-For-Tat` strategy, 
it wouldn't work properly. :code:`Tit-For-Tat` only knows of two actions (cooperate and defect,
corresponding to rows 1 and 2 respectively). If we tried to use it on rock-paper-scissors, it would
interpret the game in the following way:

1. On the first turn, choose rock (option 1, cooperate)
2. If the opponent's last move is the Python object
   :code:`axl.Action.D` (which it may never be unless the opponent also thinks it's playing IPD!), 
   then choose paper (option 2, defection)

and so as we see, :code:`Tit-For-Tat` would simply play Rock every turn, unless it
were playing against another Prisoners' Dilemma strategy (then it
plays rock unless the opponent last played paper, in which case it plays paper). In
particular, it would never play scissors - it does not know that Scissors is something
it can even do. This is not a bug, or an issue with the strategy itself; 
simply that :code:`Tit-For-Tat` *thinks* it is playing the Iterated Prisoners' Dilemma
and its :code:`Action` set, regardless of what the actual game is.

Thus, if we wanted to implement new games we should also implement a new Action set,
and some new strategies.

The Actions are relatively simple; they're an `Enum class <https://docs.python.org/3/library/enum.html>`_,
with each action corresponding to a row/column (recall that Python starts counting from 0, 
rather than 1). We can also implement some methods that we think might be useful for viewing
our actions and making strategies. (The Prisoners' Dilemma :code:`Action` class, for example, 
has :code:`flip`, which flips a :code:`C` to a :code:`D` and vice versa!)

A simple rock-paper-scissors action class would look like so::

    >>> from enum import Enum
    >>> class RPSAction(Enum):
    ...     """Actions for Rock-Paper-Scissors."""
    ...     R = 0  # rock
    ...     P = 1  # paper
    ...     S = 2  # scissors
    ...     
    ...     def __repr__(self):
    ...         return self.name
    ...     
    ...     def __str__(self):
    ...         return self.name
    ...     
    ...     def rotate(self):
    ...         """
    ...         Cycles one step through the actions.
    ...         Maps R->P, P->S, S->R
    ...         """
    ...         rotations = {
    ...             RPSAction.R: RPSAction.P,
    ...             RPSAction.P: RPSAction.S,
    ...             RPSAction.S: RPSAction.R
    ...         }
    ...         
    ...         return rotations[self]

We can then implement some strategies. Below we have the implementation of an
Axelrod strategy into Python. These follow the same format;

* A subclass of the :code:`Player` class, with three parts:

  * A :code:`name` and a :code:`classifier` dictionary. 
    This is used for indexing strategies.

  * (Optionally) an :code:`__init__` method, which allows the setting
    of initialisation variables (like probabilities of doing certain
    actions, or starting moves)

  * A :code:`strategy` method, which takes the parameters :code:`self`
    and :code:`opponent`, representing both players in the match, and provides
    the algorithm for determining the player's next move.

If we want, we can also initialise some shorthand for the actions to
avoid having to evoke their full names::

    >>> R = RPSAction.R
    >>> P = RPSAction.P
    >>> S = RPSAction.S

Here are a couple of examples. One is a strategy which copies the opponent's
previous move, and the other simply cycles through the moves. Both have
an initialisation parameter for which move they start with::

    >>> from axelrod.player import Player
    >>> class Copycat(Player):
    ...     """
    ...     Starts with a chosen move,
    ...     and then copies their opponent's previous move.
    ... 
    ...     Parameters
    ...     ----------
    ...     starting_move: RPSAction, default S
    ...         What move to play on the first round.
    ...     """
    ...     name = "Copycat"
    ...     classifier = {
    ...         "memory_depth": 1,
    ...         "stochastic": False,
    ...         "long_run_time": False,
    ...         "inspects_source": False,
    ...         "manipulates_source": False,
    ...         "manipulates_state": False,
    ...     }
    ...     
    ...     def __init__(self, starting_move=S):
    ...         self.starting_move = starting_move
    ...         super().__init__()
    ...     
    ...     def strategy(self, opponent: Player) -> RPSAction:
    ...         """Actual strategy definition that determines player's action."""
    ...         if not self.history:
    ...             return self.starting_move
    ...         return opponent.history[-1]

    >>> class Rotator(Player):
    ...     """
    ...     Cycles through the moves from a chosen starting move.
    ...     
    ...     Parameters
    ...     ----------
    ...     starting_move: RPSAction, default S
    ...         What move to play on the first round.
    ...     """
    ...     name = "Rotator"
    ...     classifier = {
    ...         "memory_depth": 1,
    ...         "stochastic": False,
    ...         "long_run_time": False,
    ...         "inspects_source": False,
    ...         "manipulates_source": False,
    ...         "manipulates_state": False,
    ...     }
    ...     
    ...     def __init__(self, starting_move=S):
    ...         self.starting_move = starting_move
    ...         super().__init__()
    ...     
    ...     def strategy(self, opponent: Player) -> RPSAction:
    ...         """Actual strategy definition that determines player's action."""
    ...         if not self.history:
    ...             return self.starting_move
    ...         return self.history[-1].rotate()

We are now all set to run some matches and tournaments in our new game!
Let's start with a match between our two new players::

    >>> match = axl.Match(players=(Copycat(starting_move=P), Rotator()),
    ...                   turns=5, 
    ...                   game=rock_paper_scissors)
    >>> match.play()
    [(P, S), (S, R), (R, P), (P, S), (S, R)]

and as with the Prisoners' Dilemma, we can run a tournament in the same way. Just
make sure you specify the game when creating the tournament!::

    >>> tournament = axl.Tournament(players, game=rock_paper_scissors)  # doctest: +SKIP
    >>> tournament.play()  # doctest: +SKIP

where :code:`players` is set to a list of Rock-Paper-Scissors strategies; hopefully
more than two, else it isn't a very interesting tournament!
