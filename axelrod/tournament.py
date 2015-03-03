from game import *
from result_set import *
from round_robin import *


class Tournament(object):
    """Reproduce Prof. Axelrod's tournament"""

    def __init__(self, players, game=None, turns=200, repetitions=10):
        """Initiate a tournmanent of players"""
        self.players = players
        self.plist = list(range(len(players)))
        if game is None:
            self.game = Game()
        else:
            self.game = game
        self.turns = turns
        self.replist = list(range(repetitions))
        self.result_set = ResultSet(
            players=players,
            repetitions=repetitions)
        self.deterministic_cache = {}

    def play(self):
        """Play the tournament with repetitions of round robin"""
        round_robin = RoundRobin(
            self.players,
            self.game, self.turns,
            self.deterministic_cache)

        for irep in self.replist:
            payoffs = round_robin.play()
            self.deterministic_cache = round_robin.deterministic_cache
            for i in self.plist:
                for j in self.plist:
                    self.result_set.results[i][j][irep] = payoffs[i][j]
        return self.result_set.results
