# -*- coding: utf-8 -*-
from .game import Game
from axelrod import Actions

C, D = Actions.C, Actions.D


def sparkline(actions, c_symbol=u'█', d_symbol=u' '):
    return u''.join([
        c_symbol if play == 'C' else d_symbol for play in actions])


class Match(object):

    def __init__(self, players, turns, deterministic_cache=None,
                 cache_mutable=True, noise=0):
        """
        Parameters
        ----------
        players : tuple
            A pair of axelrod.Player objects
        turns : integer
                The number of turns per match
        deterministic_cache : dictionary
            A cache of resulting actions for deterministic matches
        cache_mutable : boolean
            Whether the deterministic cache can be updated or not
        noise : float
            The probability that a player's intended action should be flipped
        """
        self.result = []
        self.players = list(players)
        self._classes = (players[0].__class__, players[1].__class__)
        self._turns = turns
        if deterministic_cache is None:
            self._cache = {}
        else:
            self._cache = deterministic_cache
        self._cache_mutable = cache_mutable
        self._noise = noise

    @property
    def _stochastic(self):
        """
        A boolean to show whether a match between two players would be
        stochastic
        """
        return (
            self._noise or
            any(p.classifier['stochastic'] for p in self.players)
            )

    @property
    def _cache_update_required(self):
        """
        A boolean to show whether the deterministic cache should be updated
        """
        return (
            not self._noise and
            self._cache_mutable and not (
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
        if (self._stochastic or self._classes not in self._cache):
            turn = 0
            for p in self.players:
                p.reset()
            while turn < self._turns:
                turn += 1
                self.players[0].play(self.players[1], self._noise)
            result = list(
                zip(self.players[0].history, self.players[1].history))

            if self._cache_update_required:
                self._cache[self._classes] = result
        else:
            result = self._cache[self._classes]

        self.result = result
        return result

    def scores(self, game=None):
        """Returns the scores of the previous Match plays."""
        if not game:
            game = Game()
        scores = [game.score(plays) for plays in self.result]
        return scores

    def final_score(self, game=None):
        """Returns the final score for a Match"""
        scores = self.scores(game)

        if len(scores) == 0:
            return None

        final_score = tuple(sum([score[playeri] for score in scores])
                            for playeri in [0, 1])
        return final_score

    def final_score_per_turn(self, game=None):
        """Returns the mean score per round for a Match"""
        scores = self.scores(game)

        if len(scores) == 0:
            return None

        final_score_per_turn = tuple(
            sum([score[playeri] for score in scores]) / (float(self._turns))
            for playeri in [0, 1])
        return final_score_per_turn

    def winner(self, game=None):
        """Returns the winner of the Match"""
        scores = self.final_score(game)

        if scores is not None:
            if scores[0] == scores[1]:
                return False  # No winner
            return sorted(self.players,
                          key=lambda x: scores[self.players.index(x)])[-1]
        return None

    def cooperation(self):
        """Returns the count of cooperations by each player"""

        if len(self.result) == 0:
            return None

        cooperation = tuple(sum([play[playeri] == C for play in self.result])
                            for playeri in [0, 1])
        return cooperation

    def normalised_cooperation(self):
        """Returns the count of cooperations by each player per turn"""
        cooperation = self.cooperation()

        if len(self.result) == 0:
            return None

        normalised_cooperation = tuple(
            [c / float(self._turns) for c in cooperation])

        return normalised_cooperation

    def sparklines(self, c_symbol=u'█', d_symbol=u' '):
        return (
            sparkline(self.players[0].history, c_symbol, d_symbol) +
            u'\n' +
            sparkline(self.players[1].history, c_symbol, d_symbol))

    def __len__(self):
        return self._turns
