from typing import Dict, Tuple

from axelrod import Action
from .game_params import Symm2pPosition
from .prototypes import BaseScorer, Position, Score

C, D = Action.C, Action.D
POS_1, POS_2 = Symm2pPosition.POS_1, Symm2pPosition.POS_2


# TODO(5.0): Consider making Game a part of the GameParams
class Game(BaseScorer):
    """Container for the game matrix and scoring logic.

    Attributes
    ----------
    scores: dict
        The numerical score attribute to all combinations of action pairs.
    """

    def __init__(
        self, r: Score = 3, s: Score = 0, t: Score = 5, p: Score = 1
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
        return self.scores[pair]

    def __repr__(self) -> str:
        return "Axelrod game: (R,P,S,T) = {}".format(self.RPST())

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return self.RPST() == other.RPST()


DefaultGame = Game()
