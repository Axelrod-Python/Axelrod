from game import *
from round_robin import *


class Tournament(object):
    """Reproduce Prof. Axelrod's tournament"""

    def __init__(self, players, game=None, turns=200, repetitions=10):
        """Initiate a tournmanent of players"""
        self.players = players
        self.nplayers = len(players)
        self.plist = list(range(self.nplayers))
        if game is None:
            self.game = Game()
        else:
            self.game = game
        self.turns = turns
        self.replist = list(range(repetitions))
        self.results = self.initialise_results()
        self.deterministic_cache = {}

    def initialise_results(self):
        """
        Build the initial results containing just zeros. This is an embedded
        that could be made more efficient using a NumPy array.
        """
        results = [[[0 for irep in self.replist] for j in self.plist]
                   for i in self.plist]
        return results

    def play(self):
        """Play the tournament with repetitions of round robin"""
        round_robin = RoundRobin(self.players, self.game, self.turns, self.deterministic_cache)
        for irep in self.replist:
            payoffs = round_robin.play()
            self.deterministic_cache = round_robin.deterministic_cache
            for i in self.plist:
                for j in self.plist:
                    self.results[i][j][irep] = payoffs[i][j]
        return self.results
