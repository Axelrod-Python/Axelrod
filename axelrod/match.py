# -*- coding: utf-8 -*-


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
        self._player1 = players[0]
        self._player2 = players[1]
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
            self._player1.classifier['stochastic'] or
            self._player2.classifier['stochastic'])

    @property
    def _cache_update_required(self):
        """
        A boolean to show whether the determinstic cache should be updated
        """
        return (
            not self._noise and
            self._cache_mutable and not (
                self._player1.classifier['stochastic'] or
                self._player2.classifier['stochastic'])
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
            self._player1.reset()
            self._player2.reset()
            while turn < self._turns:
                turn += 1
                self._player1.play(self._player2, self._noise)
            result = list(zip(self._player1.history, self._player2.history))

            if self._cache_update_required:
                self._cache[self._classes] = result
        else:
            result = self._cache[self._classes]

        self.result = result
        return result

    def sparklines(self, c_symbol=u'█', d_symbol=u' '):
        return (
            sparkline(self._player1.history, c_symbol, d_symbol) +
            u'\n' +
            sparkline(self._player2.history, c_symbol, d_symbol))
