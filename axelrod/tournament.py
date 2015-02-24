"""
Recreate Axelrod's tournament


"""

import inspect
import itertools


class Axelrod:
    """
    A class for an iterated prisoner's dilemma.

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
        """
        Initiate a tournament of players
        """
        self.players = list(args)
        self.deterministic_cache = {}

    def round_robin(self, turns=200):
        """
        Plays a round robin where each match lasts turns.

        We can cache scores for paris of deterministic strategies, since the outcome
        will always be the same. There are many possible keys to cache by, but perhaps
        the most versatile is a tuple with the classes of both players.
        """
        for p1, p2 in itertools.combinations(self.players, 2):
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
            p1.score += scores[0]
            p2.score += scores[1]

    def tournament(self, turns=200, repetitions=10):
        """
        Runs repetitions of the round robin (this is mainly to handle stochastic strategies).

        Returns a dictionary containing the scores for every repetition.
        """
        dic = {player:[] for player in self.players}
        for repetition in range(repetitions):
            self.round_robin(turns=turns)
            for player in self.players:
                dic[player].append(player.score)  # Record score
                player.score = 0  # Reset score
        return dic

    def calculate_scores(self, p1, p2):
        """
        Calculates the score for two players based their history and on following:

        - C vs C both get 2
        - D vs D both get 4
        - C vs D => C gets 5 and D gets 0
        """

        scores = {
            ('C', 'C'): (2, 2),
            ('D', 'D'): (4, 4),
            ('C', 'D'): (5, 0),
            ('D', 'C'): (0, 5),
        }
        s1, s2 = 0, 0

        for pair in zip(p1.history, p2.history):
            score = scores[pair]
            s1 += score[0]
            s2 += score[1]
        return s1, s2


class Player(object):
    """An abstract class for a player"""

    name = "Player"

    def __init__(self):
        """
        Initiates an empty history and 0 score for every player
        """
        self.history = []
        self.score = 0
        self.stochastic = "random" in inspect.getsource(self.__class__)

    def play(self, opponent):
        """
        This pits two players against each other: note that this will raise
        an error if no strategy method is defined (which are defined through
        class inheritance).
        """
        s1, s2 = self.strategy(opponent), opponent.strategy(self)
        self.history.append(s1)
        opponent.history.append(s2)

    def reset(self):
        """
        Resets history.
        When creating strategies that create new attributes then this method should be re-written (in the inherited class) and should not only reset history but also rest all other attributes.
        """
        self.history = []

    def strategy(self, opponent):
        """This is a placeholder"""
        return None

    def __repr__(self):
        """The string method for the strategy."""
        return self.name
