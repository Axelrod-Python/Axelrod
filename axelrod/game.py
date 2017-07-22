from .action import Action
from typing import Tuple, Union

C, D = Action.C, Action.D

Score = Union[int, float]


class Game(object):
    """A class to hold the game matrix and to score a game accordingly."""

    def __init__(self, r: Score=3, s: Score=0, t: Score=5, p: Score=1) -> None:
        self.scores = {
            (C, C): (r, r),
            (D, D): (p, p),
            (C, D): (s, t),
            (D, C): (t, s),
        }

    def RPST(self) -> Tuple[Score, Score, Score, Score]:
        """Return the values in the game matrix in the Press and Dyson
        notation."""
        R = self.scores[(C, C)][0]
        P = self.scores[(D, D)][0]
        S = self.scores[(C, D)][0]
        T = self.scores[(D, C)][0]
        return (R, P, S, T)

    def score(self, pair: Tuple[Action, Action]) -> Tuple[Score, Score]:
        """Return the appropriate score for decision pair.

        Returns the appropriate score (as a tuple) from the scores dictionary
        for a given pair of plays (passed in as a tuple).
        e.g. score((C, C)) returns (2, 2)
        """
        return self.scores[pair]

    def __repr__(self) -> str:
        return "Axelrod game: (R,P,S,T) = {}".format(self.RPST())

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return self.RPST() == other.RPST()


DefaultGame = Game()
