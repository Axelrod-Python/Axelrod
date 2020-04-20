from typing import Tuple, Union

import axelrod as axl

Score = Union[int, float]


class BaseGame(object):
    """Container for the scoring logic."""

    def __init__(self) -> None:
        """Create a new game object."""
        pass

    def score(self, pair: Tuple[axl.Action, axl.Action]) -> Tuple[Score, Score]:
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
        raise NotImplementedError()
