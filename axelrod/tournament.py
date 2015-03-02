"""Recreate Axelrod's tournament."""

import inspect


class Game(object):
    """A class to hold the game matrix and to score a game accordingly."""

    def __init__(self, r=2, s=0, t=5, p=4):
        self.scores = {
            ('C', 'C'): (r, r),
            ('D', 'D'): (p, p),
            ('C', 'D'): (t, s),
            ('D', 'C'): (s, t),
        }

    def score(self, pair):
        """Return the appropriate score for decision pair.

        Returns the appropriate score (as a tuple) from the scores dictionary
        for a given pair of plays (passed in as a tuple).
        e.g. score(('C', 'C')) returns (2, 2)
        """
        return self.scores[pair]


class RoundRobin(object):
    """A class to define play a round robin game of players"""

    def __init__(self, players, game, turns, deterministic_cache):
        """Initialise the players, game and deterministic cache"""
        self.players = players
        self.nplayers = len(players)
        self.game = game
        self.turns = turns
        self.deterministic_cache = deterministic_cache

    def calculate_scores(self, p1, p2):
        """Calculates the score for two players based their history"""
        s1, s2 = 0, 0
        for pair in zip(p1.history, p2.history):
            score = self.game.score(pair)
            s1 += score[0]
            s2 += score[1]
        return s1, s2

    def play(self):
        """Plays a round robin where each match lasts turns.

        We can cache scores for paris of deterministic strategies, since the outcome
        will always be the same. There are many possible keys to cache by, but perhaps
        the most versatile is a tuple with the classes of both players.

        Returns the total payoff matrix and the deterministic cache.
        """
        payoffs = [[0 for j in range(self.nplayers)] for i in range(self.nplayers)]

        for ip1 in range(self.nplayers):
            for ip2 in range(ip1 + 1, self.nplayers):

                p1 = self.players[ip1]
                p2 = self.players[ip2]

                cl1 = p1.__class__
                cl2 = p2.__class__
                key = (cl1, cl2)
                if (p1.stochastic or p2.stochastic or key not in self.deterministic_cache):
                    turn = 0
                    p1.reset()
                    p2.reset()
                    while turn < self.turns:
                        turn += 1
                        p1.play(p2)
                    scores = self.calculate_scores(p1, p2)
                    if not (p1.stochastic or p2.stochastic):
                        self.deterministic_cache[key] = scores
                else:
                    scores = self.deterministic_cache[key]

                payoffs[ip1][ip2] = scores[0]
                payoffs[ip2][ip1] = scores[1]

        return payoffs, self.deterministic_cache


class Tournament(object):

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
            payoffs, self.deterministic_cache = round_robin.play()
            for i in self.plist:
                for j in self.plist:
                    self.results[i][j][irep] = payoffs[i][j]
        return self.results


class Player(object):
    """An class for a player in the tournament.

    This is an abstract base class, not intended to be used directly.
    """

    name = "Player"

    def __init__(self):
        """Initiates an empty history and 0 score for a player."""
        self.history = []
        self.stochastic = "random" in inspect.getsource(self.__class__)

    def play(self, opponent):
        """This pits two players against each other.
        """
        s1, s2 = self.strategy(opponent), opponent.strategy(self)
        self.history.append(s1)
        opponent.history.append(s2)

    def reset(self):
        """Resets history.

        When creating strategies that create new attributes then this method should be
        re-written (in the inherited class) and should not only reset history but also
        rest all other attributes.
        """
        self.history = []

    def strategy(self, opponent):
        """This is a placeholder strategy."""
        return None

    def __repr__(self):
        """The string method for the strategy."""
        return self.name
