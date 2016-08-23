from __future__ import division
from math import ceil, log
import random


class MatchGenerator(object):

    def __init__(self, players, turns, game, repetitions, noise=0):
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
        noise : float, 0
            The probability that a player's intended action should be flipped
        """
        self.players = players
        self.turns = turns
        self.game = game
        self.repetitions = repetitions
        self.noise = noise
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

    def build_match_chunks(self):
        """
        A generator that returns player index pairs and match parameters for a
        round robin tournament.

        Yields
        -------
        tuples
            ((player1 index, player2 index), match object)
        """
        for player1_index in range(len(self.players)):
            for player2_index in range(player1_index, len(self.players)):
                match_params = self.build_single_match_params()
                index_pair = (player1_index, player2_index)
                yield (index_pair, match_params, self.repetitions)

    def build_single_match_params(self):
        """
        Creates a single set of match parameters.
        """
        cache = None
        return (self.turns, self.game, cache, self.noise)

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

    def __init__(self, players, prob_end, game, repetitions, noise=0):
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
        repetitions : int
            The number of repetitions of a given match
        noise : float, 0
            The probability that a player's intended action should be flipped
        """
        super(ProbEndRoundRobinMatches, self).__init__(
            players, turns=float("inf"), game=game, repetitions=repetitions,
            noise=noise)
        self.prob_end = prob_end

    def build_single_match_params(self):
        """
        Creates a single set of match parameters.
        """
        return (
            self.sample_length(), self.game, None, self.noise,
            {'length': float('inf'), 'game': self.game, 'noise': self.noise})

    def sample_length(self):
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


def graph_is_connected(edges, players):
    """
    Test if a set of edges defines a complete graph on a set of players.

    This is used by the spatial tournaments.

    Parameters:
    -----------
    edges : a list of 2 tuples
    players : a list of player names

    Returns:
    --------
    boolean : True if the graph is connected
    """
    # Check if all players are connected.
    player_indices = set(range(len(players)))
    node_indices = set()
    for edge in edges:
        for node in edge:
            node_indices.add(node)

    return player_indices == node_indices



class SpatialMatches(RoundRobinMatches):
    """
    A class that generates spatially-structured matches.
    In these matches, players interact only with their neighbors rather than the
    entire population. This reduces to a well-mixed population when the spatial
    graph is a complete graph.

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
    edges : list
        A list of tuples containing the existing edges
    """

    def __init__(self, players, turns, game, repetitions, edges, noise=0):

        if not graph_is_connected(edges, players):
            raise ValueError("The graph edges do not include all players.")
        self.edges = edges
        super(SpatialMatches, self).__init__(players, turns, game, repetitions,
                                             noise)

    def build_match_chunks(self):
        for edge in self.edges:
            match_params = self.build_single_match_params()
            index_pair = edge
            yield (index_pair, match_params, self.repetitions)

    def __len__(self):
        return len(self.edges)


class ProbEndSpatialMatches(SpatialMatches, ProbEndRoundRobinMatches):
    """
    A class that generates spatially-structured prob ending matches.
    In these matches, players interact only with their neighbors rather than the
    entire population. This reduces to a well-mixed population when the spatial
    graph is a complete graph.

    Parameters
    ----------
    players : list
        A list of axelrod.Player objects
    prob_end : float
        The probability that a turn of a Match is the last
    game : axelrod.Game
        The game object used to score the match
    repetitions : int
        The number of repetitions of a given match
    edges : list
        A list of tuples containing the existing edges
    """

    def __init__(self, players, prob_end, game, repetitions, noise, edges):

        if not graph_is_connected(edges, players):
            raise ValueError("The graph edges do not include all players.")
        self.edges = edges
        ProbEndRoundRobinMatches.__init__(self, players, prob_end,
                                          game, repetitions, noise)

    def build_single_match_params(self):
        """
        Creates a single set of match parameters.
        """
        return ProbEndRoundRobinMatches.build_single_match_params(self)
