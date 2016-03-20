import random
from math import ceil, log

from .match import Match


class TournamentType(object):

    clone_opponents = True

    def __init__(self, players, turns, deterministic_cache):
        """
        A class to represent a type of tournament and build the set of matches
        accordingly.

        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        turns : integer
            The number of turns per match
        deterministic_cache : dictionary
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


class RoundRobin(TournamentType):

    clone_opponents = True

    def build_matches(self, cache_mutable=True, noise=0):
        """
        Create a dictionary of match objects for a round robin tournament.

        Parameters
        ----------
        cache_mutable : boolean
            Whether the deterministic cache should be updated
        noise : float
            The probability that a player's intended action should be flipped

        Returns
        -------
        dictionary
            Mapping a tuple of player index numbers to an axelrod Match object
        """
        matches = {}
        for player1_index in range(len(self.players)):
            for player2_index in range(player1_index, len(self.players)):
                pair = (
                    self.players[player1_index], self.opponents[player2_index])
                match = Match(
                    pair, self.turns, self.deterministic_cache,
                    cache_mutable, noise)
                matches[(player1_index, player2_index)] = match
        return matches


class ProbEndRoundRobin(TournamentType):

    clone_opponents = True

    def __init__(self, players, prob_end, deterministic_cache):
        """
        A class to represent a tournament type for which the players do not
        know the length of the Match (to their knowledge it is infinite) but
        that ends with given probability.

        Parameters
        ----------
        players : list
            A list of axelrod.Player objects
        prob_end : float
            The probability that a turn of a Match is the last
        deterministic_cache : dictionary
            A cache of resulting actions for deterministic matches
        """
        self.players = players
        self.prob_end = prob_end
        self.turns = float("inf")
        self.deterministic_cache = deterministic_cache
        self.opponents = players

    def build_matches(self, cache_mutable=True, noise=0):
        """
        Create a dictionary of match objects for a round robin tournament.

        Parameters
        ----------
        cache_mutable : boolean
            Whether the deterministic cache should be updated
        noise : float
            The probability that a player's intended action should be flipped

        Returns
        -------
        dictionary
            Mapping a tuple of player index numbers to an axelrod Match object
        """
        matches = {}
        for player1_index in range(len(self.players)):
            for player2_index in range(player1_index, len(self.players)):
                pair = (
                    self.players[player1_index], self.opponents[player2_index])
                match = Match(
                    pair, self.sample_length(self.prob_end),
                    self.deterministic_cache, cache_mutable, noise)
                matches[(player1_index, player2_index)] = match
        return matches

    def sample_length(self, prob_end):
        """
        Sample length of a game.

        This is using inverse random sample on a pdf given by:

        f(n) = p_end * (1 - p_end) ^ (n - 1)

        Which gives cdf:

        F(n) = 1 - (1 - p) ^ n

        Which gives for given x = F(n) (ie the random sample) gives n:

        n = ceil((ln(1-x)/ln(1-p)))

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
