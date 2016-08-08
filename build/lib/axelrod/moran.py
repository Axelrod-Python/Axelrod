# -*- coding: utf-8 -*-
from collections import Counter
import random

import numpy as np

from .deterministic_cache import DeterministicCache
from .match import Match, is_stochastic
from .random_ import randrange


def fitness_proportionate_selection(scores):
    """Randomly selects an individual proportionally to score.

    Parameters
    ----------
    scores: Any sequence of real numbers

    Returns
    -------
    An index of the above list selected at random proportionally to the list
    element divided by the total.
    """
    csums = np.cumsum(scores)
    total = csums[-1]
    r = random.random() * total

    for i, x in enumerate(csums):
        if x >= r:
            return i


class MoranProcess(object):
    def __init__(self, players, turns=100, noise=0, deterministic_cache=None):
        self.turns = turns
        self.noise = noise
        self.initial_players = players  # save initial population
        self.players = []
        self.populations = []
        self.set_players()
        self.score_history = []
        self.winning_strategy_name = None
        if deterministic_cache is not None:
            self.deterministic_cache = deterministic_cache
        else:
            self.deterministic_cache = DeterministicCache()

    def set_players(self):
        """Copy the initial players into the first population."""
        self.players = []
        for player in self.initial_players:
            player.reset()
            self.players.append(player)
        self.populations = [self.population_distribution()]
        self.num_players = len(self.players)

    @property
    def _stochastic(self):
        """
        A boolean to show whether a match between two players would be
        stochastic
        """
        return is_stochastic(self.players, self.noise)

    def __next__(self):
        """Iterate the population:
        - play the round's matches
        - chooses a player proportionally to fitness (total score) to reproduce
        - choose a player at random to be replaced
        - update the population
        """
        # Check the exit condition, that all players are of the same type.
        classes = set(p.__class__ for p in self.players)
        if len(classes) == 1:
            self.winning_strategy_name = str(self.players[0])
            raise StopIteration
        scores = self._play_next_round()
        # Update the population
        # Fitness proportionate selection
        j = fitness_proportionate_selection(scores)
        # Randomly remove a strategy
        i = randrange(0, len(self.players))
        # Replace player i with clone of player j
        self.players[i] = self.players[j].clone()
        self.populations.append(self.population_distribution())

    def _play_next_round(self):
        """Plays the next round of the process. Every player is paired up
        against every other player and the total scores are recorded."""
        N = self.num_players
        scores = [0] * N
        for i in range(N):
            for j in range(i + 1, N):
                player1 = self.players[i]
                player2 = self.players[j]
                match = Match(
                    (player1, player2), turns=self.turns, noise=self.noise,
                    deterministic_cache=self.deterministic_cache)
                match.play()
                match_scores = np.sum(match.scores(), axis=0) / float(self.turns)
                scores[i] += match_scores[0]
                scores[j] += match_scores[1]
        self.score_history.append(scores)
        return scores

    def population_distribution(self):
        """Returns the population distribution of the last iteration."""
        player_names = [str(player) for player in self.players]
        counter = Counter(player_names)
        return counter

    next = __next__  # Python 2

    def __iter__(self):
        return self

    def reset(self):
        """Reset the process to replay."""
        self.winning_strategy_name = None
        self.score_history = []
        # Reset all the players
        self.set_players()

    def play(self):
        """Play the process out to completion."""
        while True:
            try:
                self.__next__()
            except StopIteration:
                break
        return self.populations

    def __len__(self):
        return len(self.populations)
