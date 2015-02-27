"""Recreate Axelrod's tournament."""

import inspect
import numpy


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


class Axelrod(object):
    """A class for an iterated prisoner's dilemma.

    Take a list of players (see the Player class):

        >>> P1 = Defector()
        >>> P2 = Cooperator()
        >>> axelrod = Axelrod(P1, P2)
        >>> axelrod.round_robin(turns=10)
        >>> for player in sorted(axelrod.players, key=lambda x: x.score):
        ...     print player, player.score
        Defector 0
        Cooperator 50
    """

    def __init__(self, *args):
        """Initiate a tournament of players."""

        self.players = list(args)
        self.nplayers = len(self.players)
        self.names = [str(p) for p in self.players]

        self.deterministic_cache = {}
        self.game = Game()

    def tournament(self, turns=200, repetitions=10):
        """Runs repetitions of a round robin tournament.

        The repetitions are mainly to handle stochastic strategies, so a cache
        is used for pairs of deterministic strategies (result always the same).

        Return the total payoff matrices for each repetition.
        """

        shape = (self.nplayers, self.nplayers, repetitions)
        payoffs = numpy.zeros(shape, dtype='int')

        for i in range(repetitions):
            payoffs[:, :, i] = self.round_robin(turns=turns)

        return payoffs

    def round_robin(self, turns=200):
        """Plays a round robin where each match lasts turns.

        We can cache scores for paris of deterministic strategies, since the outcome
        will always be the same. There are many possible keys to cache by, but perhaps
        the most versatile is a tuple with the classes of both players.

        Returns the total payoff matrix.
        """

        payoffs = numpy.zeros((self.nplayers, self.nplayers))
        for ip1 in range(self.nplayers):
            for ip2 in range(ip1 + 1, self.nplayers):

                p1 = self.players[ip1]
                p2 = self.players[ip2]

                cl1 = p1.__class__
                cl2 = p2.__class__
                key = (cl1, cl2)
                if p1.stochastic or p2.stochastic or key not in self.deterministic_cache:
                    turn = 0
                    p1.reset()
                    p2.reset()
                    while turn < turns:
                        turn += 1
                        p1.play(p2)
                    scores = self.calculate_scores(p1, p2)
                    if not (p1.stochastic or p2.stochastic):
                        self.deterministic_cache[key] = scores
                else:
                    scores = self.deterministic_cache[key]

                payoffs[ip1, ip2] = scores[0]
                payoffs[ip2, ip1] = scores[1]

        return payoffs

    def calculate_scores(self, p1, p2):
        """Calculates the score for two players based their history and on following:

        - C vs C both get 2
        - D vs D both get 4
        - C vs D => C gets 5 and D gets 0
        """
        s1, s2 = 0, 0

        for pair in zip(p1.history, p2.history):
            score = self.game.score(pair)
            s1 += score[0]
            s2 += score[1]
        return s1, s2


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
