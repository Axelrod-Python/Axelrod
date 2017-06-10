from axelrod.actions import Actions
from axelrod.game import Game
from axelrod import DEFAULT_TURNS
import axelrod.interaction_utils as iu
from .deterministic_cache import DeterministicCache
import random
from math import ceil, log


C, D = Actions.C, Actions.D


def is_stochastic(players, noise):
    """Determines if a match is stochastic -- true if there is noise or if any
    of the players involved is stochastic."""
    return (noise or any(p.classifier['stochastic'] for p in players))


class Match(object):

    def __init__(self, players, turns=None, prob_end=None,
                 game=None, deterministic_cache=None,
                 noise=0, match_attributes=None):
        """
        Parameters
        ----------
        players : tuple
            A pair of axelrod.Player objects
        turns : integer
            The number of turns per match
        prob_end : float
            The probability of a given turn ending a match
        game : axelrod.Game
            The game object used to score the match
        deterministic_cache : axelrod.DeterministicCache
            A cache of resulting actions for deterministic matches
        noise : float
            The probability that a player's intended action should be flipped
        match_attributes : dict
            Mapping attribute names to values which should be passed to players.
            The default is to use the correct values for turns, game and noise
            but these can be overridden if desired.
        """

        defaults = {(True, True): (DEFAULT_TURNS, 0),
                    (True, False): (float('inf'), prob_end),
                    (False, True): (turns, 0),
                    (False, False): (turns, prob_end)}
        self.turns, self.prob_end = defaults[(turns is None, prob_end is None)]

        self.result = []
        self.noise = noise

        if game is None:
            self.game = Game()
        else:
            self.game = game

        if deterministic_cache is None:
            self._cache = DeterministicCache()
        else:
            self._cache = deterministic_cache

        if match_attributes is None:
            known_turns = self.turns if prob_end is None else float('inf')
            self.match_attributes = {
                'length': known_turns,
                'game': self.game,
                'noise': self.noise
            }
        else:
            self.match_attributes = match_attributes

        self.players = list(players)

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, players):
        """Ensure that players are passed the match attributes"""
        newplayers = []
        for player in players:
            player.set_match_attributes(**self.match_attributes)
            newplayers.append(player)
        self._players = newplayers

    @property
    def _stochastic(self):
        """
        A boolean to show whether a match between two players would be
        stochastic.
        """
        return is_stochastic(self.players, self.noise)

    @property
    def _cache_update_required(self):
        """
        A boolean to show whether the deterministic cache should be updated.
        """
        return (
            not self.noise and
            self._cache.mutable and not (
                any(p.classifier['stochastic'] for p in self.players)
            )
        )

    def play(self):
        """
        The resulting list of actions from a match between two players.

        This method determines whether the actions list can be obtained from
        the deterministic cache and returns it from there if so. If not, it
        calls the play method for player1 and returns the list from there.

        Returns
        -------
        A list of the form:

        e.g. for a 2 turn match between Cooperator and Defector:

            [(C, C), (C, D)]

        i.e. One entry per turn containing a pair of actions.
        """
        turns = min(sample_length(self.prob_end), self.turns)
        cache_key = (self.players[0], self.players[1], turns)

        if self._stochastic or (cache_key not in self._cache):
            for p in self.players:
                p.reset()
            for _ in range(turns):
                self.players[0].play(self.players[1], self.noise)
            result = list(
                zip(self.players[0].history, self.players[1].history))

            if self._cache_update_required:
                self._cache[cache_key] = result
        else:
            result = self._cache[cache_key]

        self.result = result
        return result

    def scores(self):
        """Returns the scores of the previous Match plays."""
        return iu.compute_scores(self.result, self.game)

    def final_score(self):
        """Returns the final score for a Match."""
        return iu.compute_final_score(self.result, self.game)

    def final_score_per_turn(self):
        """Returns the mean score per round for a Match."""
        return iu.compute_final_score_per_turn(self.result, self.game)

    def winner(self):
        """Returns the winner of the Match."""
        winner_index = iu.compute_winner_index(self.result, self.game)
        if winner_index is False:  # No winner
            return False
        if winner_index is None:  # No plays
            return None
        return self.players[winner_index]

    def cooperation(self):
        """Returns the count of cooperations by each player."""
        return iu.compute_cooperations(self.result)

    def normalised_cooperation(self):
        """Returns the count of cooperations by each player per turn."""
        return iu.compute_normalised_cooperation(self.result)

    def state_distribution(self):
        """
        Returns the count of each state for a set of interactions.
        """
        return iu.compute_state_distribution(self.result)

    def normalised_state_distribution(self):
        """
        Returns the normalized count of each state for a set of interactions.
        """
        return iu.compute_normalised_state_distribution(self.result)

    def sparklines(self, c_symbol='█', d_symbol=' '):
        return iu.compute_sparklines(self.result, c_symbol, d_symbol)

    def __len__(self):
        return self.turns


def sample_length(prob_end):
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
    if prob_end == 0:
        return float("inf")
    if prob_end == 1:
        return 1
    x = random.random()
    return int(ceil(log(1 - x) / log(1 - prob_end)))
