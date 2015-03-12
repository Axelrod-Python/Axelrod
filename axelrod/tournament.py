from game import *
from result_set import *
from round_robin import *


class Tournament(object):
    """Reproduce Prof. Axelrod's tournament"""

    game = Game()

    def __init__(self, players, game=None, turns=200, repetitions=10):
        """Initiate a tournmanent of players"""

        self.players = players
        self.nplayers = len(self.players)

        if game is not None:
            self.game = game
        self.turns = turns
        self.repetitions = repetitions

        self.result_set = ResultSet(
            players=players,
            turns=turns,
            repetitions=repetitions)

        self.deterministic_cache = {}

    def play(self):
        """Play the tournament with repetitions of round robin"""

        round_robin = RoundRobin(
            self.players,
            self.game,
            self.turns,
            self.deterministic_cache)
        plist = list(range(len(self.players)))
        replist = list(range(self.repetitions))

        for irep in replist:
            payoffs = round_robin.play()
            self.deterministic_cache = round_robin.deterministic_cache
            for i in plist:
                for j in plist:
                    self.result_set.results[i][j][irep] = payoffs[i][j]

        return self.result_set
