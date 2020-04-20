from typing import Dict, List, Tuple, Union

import axelrod as axl
from axelrod.game import BaseGame
from axelrod.player import BasePlayer

Score = Union[int, float]


class BaseMatch(object):
    """The BaseMatch class conducts matches between two players."""

    def __init__(
        self,
        players: Tuple[BasePlayer],
        turns: int = None,
        prob_end: float = None,
        game: BaseGame = None,
        noise: float = 0,
        match_attributes: Dict = None,
        reset: bool = True,
    ):
        """
        Needs to be overwritten in derived class.

        Parameters
        ----------
        players : tuple
            A pair of axelrodPlayer objects
        turns : integer
            The number of turns per match
        prob_end : float
            The probability of a given turn ending a match
        game : axelrod.BaseGame
            The game object used to score the match
        noise : float
            The probability that a player's intended action should be flipped
        match_attributes : dict
            Mapping attribute names to values which should be passed to players.
            The default is to use the correct values for turns, game and noise
            but these can be overridden if desired.
        reset : bool
            Whether to reset players or not
        """
        pass

    @property
    def players(self) -> Tuple[BasePlayer]:
        raise NotImplementedError()

    def play(self) -> List[Tuple[axl.Action]]:
        """The resulting list of actions from a match between two players."""
        raise NotImplementedError()

    def scores(self) -> List[Score]:
        """Returns the scores of the previous BaseMatch plays."""
        raise NotImplementedError()

    def final_score(self) -> Score:
        """Returns the final score for a BaseMatch."""
        raise NotImplementedError()

    def final_score_per_turn(self) -> Score:
        """Returns the mean score per round for a BaseMatch."""
        raise NotImplementedError()

    def winner(self) -> BasePlayer:
        """Returns the winner of the IpdMatch."""
        raise NotImplementedError()

    def __len__(self) -> int:
        """Number of turns in the match"""
        raise NotImplementedError()
