from typing import List, Tuple

import axelrod as axl
from axelrod.player import BasePlayer
from axelrod.game import BaseGame


class BaseTournament(object):
    def __init__(
        self,
        players: List[BasePlayer],
        name: str = "axelrod",
        game: BaseGame = None,
        turns: int = None,
        prob_end: float = None,
        repetitions: int = 10,
        noise: float = 0,
        edges: List[Tuple] = None,
        match_attributes: dict = None,
    ) -> None:
        """
        Parameters
        ----------
        players : list
            A list of axelrodPlayer objects
        name : string
            A name for the tournament
        game : axelrod.IpdGame
            The game object used to score the tournament
        turns : integer
            The number of turns per match
        prob_end : float
            The probability of a given turn ending a match
        repetitions : integer
            The number of times the round robin should be repeated
        noise : float
            The probability that a player's intended action should be flipped
        prob_end : float
            The probability of a given turn ending a match
        edges : list
            A list of edges between players
        match_attributes : dict
            Mapping attribute names to values which should be passed to players.
            The default is to use the correct values for turns, game and noise
            but these can be overridden if desired.
        """
        pass

    def setup_output(self, filename=None):
        """assign/create `filename` to `self`. If file should be deleted once
        `play` is finished, assign a file descriptor. """
        raise NotImplementedError()

    def play(
        self,
        build_results: bool = True,
        filename: str = None,
        processes: int = None,
        progress_bar: bool = True,
    ) -> axl.ResultSet:
        """
        Plays the tournament and passes the results to the ResultSet class

        Parameters
        ----------
        build_results : bool
            whether or not to build a results set
        filename : string
            name of output file
        processes : integer
            The number of processes to be used for parallel processing
        progress_bar : bool
            Whether or not to create a progress bar which will be updated

        Returns
        -------
        axelrod.ResultSet
        """
        raise NotImplementedError()
