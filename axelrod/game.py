from typing import Tuple, Union

import numpy as np

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
    def __init__(self, A: np.array, B: np.array) -> None:
        """
        Creates an asymmetric game from two matrices.

        Parameters
        ----------
        A: np.array
            the payoff matrix for player A.
        B: np.array
            the payoff matrix for player B.
        """

        self.scores = {
            (C, C): (A[0][0], B[0][0]),
            (D, D): (A[1][1], B[1][1]),
            (C, D): (A[0][1], B[0][1]),
            (D, C): (A[1][0], B[1][0]),
        }

        self.A = A
        self.B = B

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
        # handle being passed Actions, or a mix of Actions and ints
        actions_to_ints = {C: 0, D: 1}

        def convert_action(x):
            if isinstance(x, Action):
                return actions_to_ints[x]
            return x

        r, c = map(convert_action, pair)

        # the '.item()' method converts the values from Numpy datatypes
        # to native Python ones for compatibility
        return (self.A[r][c].item(), self.B[r][c].item())

    def __repr__(self) -> str:
        return "Axelrod game with matrices = {}".format((self.A, self.B))

    def __eq__(self, other):
        if not isinstance(other, Game):
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

    def __init__(self, r: Score = 3, s: Score = 0, t: Score = 5, p: Score = 1) -> None:
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
