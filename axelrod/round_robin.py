from __future__ import division


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

    def _stochastic_interaction(self, p1, p2):
        return (
            self._noise or
            p1.stochastic or
            p2.stochastic)

    def _cache_update_required(self, p1, p2):
        return (
            not self._noise and
            self.cache_mutable and
            not (p1.stochastic or p2.stochastic))

    def _calculate_scores(self, p1, p2):
        """Calculates the score for two players based their history"""
        s1, s2 = 0, 0
        for pair in zip(p1.history, p2.history):
            score = self.game.score(pair)
            s1 += score[0]
            s2 += score[1]
        return s1, s2

    def _calculate_cooperation(self, player):
        return player.history.count('C') / len(player.history)

    def _empty_matrix(self, rows, columns):
        return [[0 for j in range(columns)] for i in range(rows)]

    def _pair_of_players(self, player1_index, player2_index):
        player1 = self.players[player1_index]
        class1 = player1.__class__
        if player1_index == player2_index:
            player2 = class1()
            class2 = class1
        else:
            player2 = self.players[player2_index]
            class2 = player2.__class__
        return player1, player2, (class1, class2)

    def _run_single_interaction(self, player1_index, player2_index, payoffs,
                                cooperation):
        player1, player2, key = self._pair_of_players(
            player1_index, player2_index)
        play_required = (
            self._stochastic_interaction(player1, player2) or
            key not in self.deterministic_cache)
        if play_required:
            scores, cooperation_rates = self._play_single_interaction(
                player1, player2, key)
        else:
            scores = self.deterministic_cache[key]
            cooperation_rates = (0, 0)

        # For self-interactions we can take the average of the two
        # sides, which should improve the averaging a bit.
        if not self._noise and player1_index == player2_index:
            payoffs[player1_index][player2_index] = (
                0.5 * (scores[0] + scores[1]))
        else:
            payoffs[player1_index][player2_index] = scores[0]
            payoffs[player2_index][player1_index] = scores[1]

        cooperation[player1_index][player2_index] = cooperation_rates[0]
        cooperation[player2_index][player1_index] = cooperation_rates[1]

    def _play_single_interaction(self, player1, player2, key):
        turn = 0
        player1.reset()
        player2.reset()
        while turn < self.turns:
            turn += 1
            player1.play(player2, self._noise)
        scores = self._calculate_scores(player1, player2)
        cooperation_rates = (
            self._calculate_cooperation(player1),
            self._calculate_cooperation(player2))
        if self._cache_update_required(player1, player2):
            self.deterministic_cache[key] = scores
        return scores, cooperation_rates

    def play(self):
        """Plays a round robin where each match lasts turns.

        We cache scores for pairs of deterministic strategies, since the
        outcome will always be the same.

        Notice also that we need to handle self-interactions with some special
        exceptions due to the way gameplay is coded within Player.

        Returns the total payoff matrix.
        """

        payoffs = self._empty_matrix(self.nplayers, self.nplayers)
        cooperation = self._empty_matrix(self.nplayers, self.nplayers)

        for player1_index in range(self.nplayers):
            for player2_index in range(player1_index, self.nplayers):
                self._run_single_interaction(
                    player1_index, player2_index, payoffs, cooperation)

        self.payoffs = payoffs
        self.cooperation = cooperation

        return self.payoffs
