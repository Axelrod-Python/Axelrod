from __future__ import division
from axelrod import Actions

class RoundRobin(object):
    """A class to define play a round robin game of players"""

    def __init__(self, players, game, turns, deterministic_cache=None,
                 cache_mutable=True, noise=0):
        """Initialise the players, game and deterministic cache"""
        self.players = players
        self.nplayers = len(players)
        self.game = game
        self.turns = turns
        if deterministic_cache is None:
            self.deterministic_cache = {}
        else:
            self.deterministic_cache = deterministic_cache
        self.cache_mutable = cache_mutable
        self._noise = noise

    def play(self):
        """Plays a round robin where each match lasts turns.

        We cache scores for pairs of deterministic strategies, since the
        outcome will always be the same.

        Notice also that we need to handle self-interactions with some special
        exceptions due to the way gameplay is coded within Player.

        Returns the total payoff matrix.
        """
        for player1_index in range(self.nplayers):
            for player2_index in range(player1_index, self.nplayers):
                pass
        return

    def _single_interaction(self, player1_index, player2_index):
        player1, player2, classes = self._pair_of_players(
            player1_index, player2_index)
        play_required = (
            self._stochastic_interaction(player1, player2) or
            classes not in self.deterministic_cache)
        if play_required:
            pass
        else:
            pass
        return

    def _pair_of_players(self, player1_index, player2_index):
        player1 = self.players[player1_index]
        class1 = player1.__class__
        if player1_index == player2_index:
            player2 = player1.clone()
        else:
            player2 = self.players[player2_index]
        class2 = player2.__class__
        return player1, player2, (class1, class2)

    def _stochastic_interaction(self, player1, player2):
        return (
            self._noise or
            player1.classifier['stochastic'] or
            player2.classifier['stochastic'])

    def _play_single_interaction(self, player1, player2, classes):
        turn = 0
        player1.reset()
        player2.reset()
        while turn < self.turns:
            turn += 1
            player1.play(player2, self._noise)
        if self._cache_update_required(player1, player2):
            self.deterministic_cache[classes] = {}
        return

    def _cache_update_required(self, p1, p2):
        return (
            not self._noise and
            self.cache_mutable and
            not (p1.classifier['stochastic'] or p2.classifier['stochastic']))
