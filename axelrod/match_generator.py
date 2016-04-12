import random
from math import ceil, log

from .match import Match


class MatchGenerator(object):

    clone_opponents = True

    def __init__(self, players, turns, deterministic_cache):
        """
        A class to generate matches. This is used by the Tournament class which
        is in charge of playing the matches and collecting the results.

        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        turns : integer
            The number of turns per match
        deterministic_cache : an instance of axelrod.DeterministicCache
        class
            A cache of resulting actions for deterministic matches
        """
        self.players = players
        self.turns = turns
        self.deterministic_cache = deterministic_cache
        self.opponents = players

    @property
    def opponents(self):
        return self._opponents

    @opponents.setter
    def opponents(self, players):
        if self.clone_opponents:
            opponents = []
            for player in players:
                opponents.append(player.clone())
        else:
            opponents = players
        self._opponents = opponents

    def build_matches():
        raise NotImplementedError()

    def build_single_match():
        raise NotImplementedError()


class RoundRobinMatches(MatchGenerator):

    clone_opponents = True

    def build_matches(self, noise=0):
        """
        A generator that returns player index pairs and match objects for a
        round robin tournament.

        Parameters
        ----------
        noise : float
            The probability that a player's intended action should be flipped

        Yields
        -------
        tuple
            player pair index, match object
        """
        for player1_index in range(len(self.players)):
            for player2_index in range(player1_index, len(self.players)):
                pair = (
                    self.players[player1_index], self.opponents[player2_index])
                match = self.build_single_match(pair, noise)
                yield (player1_index, player2_index), match

    def build_single_match(self, pair, noise=0):
        """Create a single match for a given pair"""
        return Match(pair, self.turns, self.deterministic_cache, noise)


class ProbEndRoundRobinMatches(RoundRobinMatches):

    clone_opponents = True

    def __init__(self, players, prob_end, deterministic_cache):
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
        deterministic_cache : an instance of axelrod.DeterministicCache
            A cache of resulting actions for deterministic matches
        """
        super(ProbEndRoundRobinMatches, self).__init__(
            players, turns=float("inf"),
            deterministic_cache=deterministic_cache)
        self.deterministic_cache.mutable = False
        self.prob_end = prob_end

    def build_single_match(self, pair, noise=0):
        """Create a single match for a given pair"""
        return Match(pair, self.sample_length(self.prob_end),
                     self.deterministic_cache, noise)

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
