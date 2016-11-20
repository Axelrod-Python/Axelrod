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
    def __init__(self, players, turns=100, noise=0, deterministic_cache=None, mutation_rate=0.):
        """
        An agent based Moran process class. In each round, each player plays a Match with each other
        player. Players are assigned a fitness score by their total score from all matches in the round.
        A player is chosen to reproduce proportionally to fitness, possibly mutated, and is cloned. The
        clone replaces a randomly chosen player.

        If the mutation_rate is 0, the population will eventually fixate on exactly one player type. In this
        case a StopIteration exception is raised and the play stops. If mutation_rate is not zero, then
        the process will iterate indefinitely, so mp.play() will never exit, and you should use the class as an
        iterator instead.

        When a player mutates it chooses a random player type from the initial population. This is not the only
        method yet emulates the common method in the literature.

        Parameters
        ----------
        players, iterable of axelrod.Player subclasses
        turns: int, 100
            The number of turns in each pairwise interaction
        noise: float, 0
            The background noise, if any. Randomly flips plays with probability `noise`.
        deterministic_cache: axelrod.DeterministicCache, None
            A optional prebuilt deterministic cache
        mutation_rate: float, 0
            The rate of mutation. Replicating players are mutated with probability `mutation_rate`
        """
        self.turns = turns
        self.noise = noise
        self.initial_players = players  # save initial population
        self.players = []
        self.populations = []
        self.set_players()
        self.score_history = []
        self.winning_strategy_name = None
        self.mutation_rate = mutation_rate
        assert (mutation_rate >= 0) and (mutation_rate <= 1)
        assert (noise >= 0) and (noise <= 1)
        if deterministic_cache is not None:
            self.deterministic_cache = deterministic_cache
        else:
            self.deterministic_cache = DeterministicCache()
        # Build the set of mutation targets
        # Determine the number of unique types (players)
        keys = set([str(p) for p in players])
        # Create a dictionary mapping each type to a set of representatives of the other types
        d = dict()
        for p in players:
            d[str(p)] = p
        mutation_targets = dict()
        for key in sorted(keys):
            mutation_targets[key] = [v for (k, v) in sorted(d.items()) if k != key]
        self.mutation_targets = mutation_targets

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
        return is_stochastic(self.players, self.noise) or (self.mutation_rate > 0)

    def mutate(self, index):
        # If mutate, choose another strategy at random from the initial population
        r = random.random()
        if r < self.mutation_rate:
            s = str(self.players[index])
            j = randrange(0, len(self.mutation_targets[s]))
            p = self.mutation_targets[s][j]
            new_player = p.clone()
        else:
            # Just clone the player
            new_player = self.players[index].clone()
        return new_player

    def __next__(self):
        """Iterate the population:
        - play the round's matches
        - chooses a player proportionally to fitness (total score) to reproduce
        - mutate, if appropriate
        - choose a player at random to be replaced
        - update the population
        """
        # Check the exit condition, that all players are of the same type.
        classes = set(str(p) for p in self.players)
        if (self.mutation_rate == 0) and (len(classes) == 1):
            self.winning_strategy_name = str(self.players[0])
            raise StopIteration
        scores = self._play_next_round()
        # Update the population
        # Fitness proportionate selection
        j = fitness_proportionate_selection(scores)
        # Mutate?
        if self.mutation_rate:
            new_player = self.mutate(j)
        else:
            new_player = self.players[j].clone()
        # Randomly remove a strategy
        i = randrange(0, len(self.players))
        # Replace player i with clone of player j
        self.players[i] = new_player
        self.populations.append(self.population_distribution())
        return self

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
                match_scores = match.final_score_per_turn()
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
        if self.mutation_rate != 0:
            raise ValueError("MoranProcess.play() will never exit if mutation_rate is nonzero")
        while True:
            try:
                self.__next__()
            except StopIteration:
                break
        return self.populations

    def __len__(self):
        return len(self.populations)
