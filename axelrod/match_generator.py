from __future__ import division
from math import ceil, log
import random

from .match import Match


class MatchGenerator(object):

    def __init__(self, players, turns, game, repetitions):
        """
        A class to generate matches. This is used by the Tournament class which
        is in charge of playing the matches and collecting the results.

        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        turns : integer
            The number of turns per match
        game : axelrod.Game
            The game object used to score the match
        repetitions : int
            The number of repetitions of a given match
        """
        self.players = players
        self.turns = turns
        self.game = game
        self.repetitions = repetitions
        self.opponents = players

    @property
    def opponents(self):
        return self._opponents

    @opponents.setter
    def opponents(self, players):
        opponents = []
        for player in players:
            opponents.append(player.clone())
        self._opponents = opponents

    def __len__(self):
        raise NotImplementedError()

    def build_match_chunks(self):
        raise NotImplementedError()

    def build_single_match_params(self):
        raise NotImplementedError()


class RoundRobinMatches(MatchGenerator):

    def build_match_chunks(self, noise=0):
        """
        A generator that returns player index pairs and match parameters for a
        round robin tournament.

        parameters
        ----------
        noise : float, 0
            The probability that a player's intended action should be flipped

        Yields
        -------
        tuples
            ((player1 index, player2 index), match object)
        """
        for player1_index in range(len(self.players)):
            for player2_index in range(player1_index, len(self.players)):
                match_params = self.build_single_match_params(noise)
                index_pair = (player1_index, player2_index)
                yield (index_pair, match_params, self.repetitions)

    def build_single_match_params(self, noise=0):
        """
        Creates a single set of match parameters.

        parameters
        ----------
        noise : float, 0
            The probability that a player's intended action should be flipped
        """
        cache = None
        return (self.turns, self.game, cache, noise)

    def __len__(self):
        """
        The size of the generator.
        This corresponds to the number of match chunks as it
        ignores repetitions.
        """
        n = len(self.players)
        num_matches = int(n * (n - 1) // 2 + n)
        return num_matches

    def estimated_size(self):
        """Rough estimate of the number of matches that will be generated."""
        size = self.__len__() * self.turns * self.repetitions
        return size


class ProbEndRoundRobinMatches(RoundRobinMatches):

    def __init__(self, players, prob_end, game, repetitions):
        """
        A class that generates matches for which the players do not
        know the length of the Match (to their knowledge it is infinite) but
        that ends with given probability.

        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        prob_end : float
            The probability that a turn of a Match is the last
        game : axelrod.Game
            The game object used to score the match
        deterministic_cache : an instance of axelrod.DeterministicCache
            A cache of resulting actions for deterministic matches
        """
        super(ProbEndRoundRobinMatches, self).__init__(
            players, turns=float("inf"), game=game, repetitions=repetitions)
        self.prob_end = prob_end

    def build_single_match_params(self, noise=0):
        """
        Creates a single set of match parameters.

        parameters
        ----------
        noise : float, 0
            The probability that a player's intended action should be flipped
        """
        return (self.sample_length(self.prob_end), self.game, None, noise)

    def sample_length(self, prob_end):
        """
        Sample length of a game.

        This is using inverse random sample on a probability density function
        <https://en.wikipedia.org/wiki/Probability_density_function> given by:

        f(n) = p_end * (1 - p_end) ^ (n - 1)

        (So the probability of length n is given by f(n))

        Which gives cumulative distribution function
        <https://en.wikipedia.org/wiki/Cumulative_distribution_function>:

        F(n) = 1 - (1 - p_end) ^ n

        (So the probability of length less than or equal to n is given by F(n))

        Which gives for given x = F(n) (ie the random sample) gives n:

        n = ceil((ln(1-x)/ln(1-p_end)))

        This approach of sampling from a distribution is called inverse
        transform sampling
        <https://en.wikipedia.org/wiki/Inverse_transform_sampling>.

        Note that this corresponds to sampling at the end of every turn whether
        or not the Match ends.
        """
        try:
            x = random.random()
            return int(ceil(log(1 - x) / log(1 - self.prob_end)))
        except ZeroDivisionError:
            return float("inf")
        except ValueError:
            return 1

    def estimated_size(self):
        """Rough estimate of the number of matches that will be generated."""
        size = self.__len__() * (1. / self.prob_end) * self.repetitions
        return size
