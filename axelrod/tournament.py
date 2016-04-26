from __future__ import absolute_import

import logging

from .game import Game
from .result_set import ResultSet
from .parallel_matches import generate_match_parameters, play_matches_parallel


class Tournament(object):
    game = Game()

    def __init__(self, players, match_generator=RoundRobinMatches,
                 name='axelrod', game=None, turns=200, repetitions=10,
                 processes=None, deterministic_cache=None, noise=0,
                 with_morality=True):
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        match_generator : class
            A class that must be descended from axelrod.MatchGenerator
        name : string
            A name for the tournament
        game : axelrod.Game
            The game object used to score the tournament
        turns : integer
            The number of turns per match
        repetitions : integer
            The number of times the round robin should be repeated
        processes : integer
            The number of processes to be used for parallel processing
        deterministic_cache : instance
            An instance of the axelrod.DeterministicCache class
        noise : float
            The probability that a player's intended action should be flipped
        with_morality : boolean
            Whether morality metrics should be calculated
        """
        self.name = name
        self.turns = turns
        self.noise = noise
        if game is not None:
            self.game = game
        self.players = players
        self.repetitions = repetitions
        self._with_morality = with_morality
        self._processes = processes
        self._logger = logging.getLogger(__name__)

    def play(self, filename=None):
        """
        Plays the tournament and passes the results to the ResultSet class

        Returns
        -------
        axelrod.ResultSet
        """

        matches = generate_match_parameters(players, turns=self.turns,
                                            noise=self.noise,
                                            repetitions=self.repetitions,
                                            game=self.game)
        self.interactions = play_matches_parallel(matches,
                                                  filename=filename,
                                                  max_workers=self._processes)
        if self.interactions:
            self._build_result_set()

    def _build_result_set(self):
        """
        Build the result set (used by the play method)

        Returns
        -------
        axelrod.ResultSet
        """
        result_set = ResultSet(
            players=self.players,
            interactions=self.interactions,
            with_morality=self._with_morality)
        return result_set


class ProbEndTournament(Tournament):
    """
    A tournament in which the player don't know the length of a given match
    (currently implemented by setting this to be infinite). The length of a
    match is equivalent to randomly sampling after each round whether or not to
    continue.
    """

    def __init__(self, players, match_generator=ProbEndRoundRobinMatches,
                 name='axelrod', game=None, prob_end=.5, repetitions=10,
                 processes=None, deterministic_cache=None, noise=0,
                 with_morality=True):
        """
        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        match_generator : class
            A class that must be descended from axelrod.MatchGenerator
        name : string
            A name for the tournament
        game : axelrod.Game
            The game object used to score the tournament
        prob_end : a float
            The probability of a given match ending
        repetitions : integer
            The number of times the round robin should be repeated
        processes : integer
            The number of processes to be used for parallel processing
        noise : float
            The probability that a player's intended action should be flipped
        deterministic_cache : instance
            An instance of the axelrod.DeterministicCache class
        with_morality : boolean
            Whether morality metrics should be calculated
        """
        super(ProbEndTournament, self).__init__(
            players, name=name, game=game, turns=float("inf"),
            repetitions=repetitions, processes=processes,
            deterministic_cache=deterministic_cache,
            noise=noise, with_morality=with_morality)

        self.prob_end = prob_end

    def play(self, filename=None):
        """
        Plays the tournament and passes the results to the ResultSet class

        Returns
        -------
        axelrod.ResultSet
        """

        matches = generate_match_parameters(players, turns=self.turns,
                                            noise=self.noise,
                                            repetitions=self.repetitions,
                                            game=self.game,
                                            self.prob_end)
        self.interactions = play_matches_parallel(matches,
                                                  filename=filename,
                                                  max_workers=self._processes)
        if self.interactions:
            self._build_result_set()
