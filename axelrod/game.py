from enum import Enum
from typing import Tuple, Union

import numpy as np
import numpy.typing as npt

from axelrod import Action

C, D = Action.C, Action.D

Score = Union[int, float]


class AsymmetricGame(object):
    """Container for the game matrix and scoring logic.

    Attributes
    ----------
    scores: dict
        The numerical score attribute to all combinations of action pairs.
    """

    # pylint: disable=invalid-name
    def __init__(self, A: npt.NDArray, B: npt.NDArray) -> None:
        """
        Creates an asymmetric game from two matrices.

        Parameters
        ----------
        A: np.array
            the payoff matrix for player A.
        B: np.array
            the payoff matrix for player B.
        """

        if A.shape != B.transpose().shape:
            raise ValueError(
                "AsymmetricGame was given invalid payoff matrices; the shape "
                "of matrix A should be the shape of B's transpose matrix."
            )

        self.A = A
        self.B = B

        self.scores = {
            pair: self.score(pair) for pair in ((C, C), (D, D), (C, D), (D, C))
        }

    def score(
        self, pair: Union[Tuple[Action, Action], Tuple[int, int]]
    ) -> Tuple[Score, Score]:
        """Returns the appropriate score for a decision pair.
        Parameters
        ----------
        pair: tuple(int, int) or tuple(Action, Action)
            A pair of actions for two players, for example (0, 1) corresponds
            to the row player choosing their first action and the column
            player choosing their second action; in the prisoners' dilemma,
            this is equivalent to player 1 cooperating and player 2 defecting.
            Can also be a pair of Actions, where C corresponds to '0'
            and D to '1'.

        Returns
        -------
        tuple of int or float
            Scores for two player resulting from their actions.
        """

        # if an Action has been passed to the method,
        # get which integer the Action corresponds to
        def get_value(x):
            if isinstance(x, Enum):
                return x.value
            return x

        row, col = map(get_value, pair)

        return (self.A[row][col], self.B[row][col])

    def __repr__(self) -> str:
        return "Axelrod game with matrices: {}".format((self.A, self.B))

    def __eq__(self, other):
        if not isinstance(other, AsymmetricGame):
            return False
        return self.A.all() == other.A.all() and self.B.all() == other.B.all()


class Game(AsymmetricGame):
    """
    Simplification of the AsymmetricGame class for symmetric games.
    Takes advantage of Press and Dyson notation.

    Can currently only be 2x2.

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
        A = np.array([[r, s], [t, p]])

        super().__init__(A, A.transpose())

    def RPST(self) -> Tuple[Score, Score, Score, Score]:
        """Returns game matrix values in Press and Dyson notation."""
        R = self.scores[(C, C)][0]
        P = self.scores[(D, D)][0]
        S = self.scores[(C, D)][0]
        T = self.scores[(D, C)][0]
        return R, P, S, T

    def __repr__(self) -> str:
        return "Axelrod game: (R,P,S,T) = {}".format(self.RPST())

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return self.RPST() == other.RPST()


DefaultGame = Game()
