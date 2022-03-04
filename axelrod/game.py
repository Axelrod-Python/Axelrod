from typing import Tuple, Union

from axelrod import Action
from random import randint

C, D = Action.C, Action.D

Score = Union[int, float]


class Game(object):
    """Container for the game matrix and scoring logic.

    Attributes
    ----------
    scores: dict
        The numerical score attribute to all combinations of action pairs.
    """

    def __init__(
        self, r: Score = 32, s: Score = 10, t: Score = 52, p: Score = 24
    ) -> None:
        """Create a new game object.

        Parameters
        ----------
        r: int or float
            Score obtained by both players for mutual cooperation.
        s: int or float
            Score obtained by a player for cooperating against a defector.
        t: int or float
            Score obtained by a player for defecting against a cooperator.
        p: int or float
            Score obtained by both player for mutual defection.
        """
        self.scores = {
            (C, C): (r, r),
            (D, D): (p, p),
            (C, D): (s, t),
            (D, C): (t, s),
        }

    def RPST(self) -> Tuple[Score, Score, Score, Score]:
        """Returns game matrix values in Press and Dyson notation."""
        R = self.scores[(C, C)][0]
        P = self.scores[(D, D)][0]
        S = self.scores[(C, D)][0]
        T = self.scores[(D, C)][0]
        return R, P, S, T

    def score(self, pair: Tuple[Action, Action]) -> Tuple[Score, Score]:
        """Returns the appropriate score for a decision pair.

        Parameters
        ----------
        pair: tuple(Action, Action)
            A pair actions for two players, for example (C, C).

        Returns
        -------
        tuple of int or float
            Scores for two player resulting from their actions.
        """
        return self.scores[pair]

    def change_game(self, p_A: float) -> None:
        """Changes the rewards associated with each outcome to less cooperative version with a probability p_A."""
        seed = randint(1, 100)
        if seed <= 100*p_A:
            self.scores[(C, C)] = (32, 32)
            self.scores[(D, D)] = (24, 24)
            self.scores[(C, D)] = (10, 52)
            self.scores[(D, C)] = (52, 10)

        else:
            self.scores[(C, C)] = (62, 62)
            self.scores[(D, D)] = (24, 24)
            self.scores[(C, D)] = (10, 82)
            self.scores[(D, C)] = (82, 10)

    def __repr__(self) -> str:
        return "Axelrod game: (R,P,S,T) = {}".format(self.RPST())

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return self.RPST() == other.RPST()


DefaultGame = Game()
