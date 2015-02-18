"""
Recreate Axelrod's tournament


"""
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

    def round_robin(self, turns=200):
        """
        Plays a round robin where each match lasts turns.
        """
        for p1, p2 in itertools.combinations(self.players, 2):
            turn = 0
            p1.history = []
            p2.history = []
            while turn < turns:
                turn += 1
                p1.play(p2)
            scores = self.calculate_scores(p1, p2)
            p1.score += scores[0]
            p2.score += scores[1]

    def tournament(self, turns=200, repetitions=10):
        """
        Runs repetitions of the round robin (this is mainly to handle stochastic strategies).

        Returns a dictionary containing the scores for every repetition.
        """
        dic = {player:[] for player in self.players}
        for repetition in range(repetitions):
            self.reset_player_history()
            self.reset_player_scores()
            self.round_robin(turns=200)
            for player in self.players:
                dic[player].append(player.score)
        return dic

    def reset_player_history(self):
        """
        Resets all the player histories
        """
        for player in self.players:
            player.history = []

    def reset_player_scores(self):
        """
        Resets all the player histories
        """
        for player in self.players:
            player.score = 0

    def calculate_scores(self, p1, p2):
        """
        Calculates the score for two players based their history and on following:

        - C vs C both get 2
        - D vs D both get 4
        - C vs D => C gets 5 and D gets 0

            >>> P1 = Player()
            >>> P1.history = ['C', 'C', 'D']
            >>> P2 = Player()
            >>> P2.history = ['C', 'D', 'D']
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.calculate_scores(P1, P2)
            (11, 6)

            >>> P1 = Player()
            >>> P1.history = ['C', 'C', 'C']
            >>> P2 = Player()
            >>> P2.history = ['C', 'C', 'C']
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.calculate_scores(P1, P2)
            (6, 6)

            >>> P1 = Player()
            >>> P1.history = ['D', 'D', 'D']
            >>> P2 = Player()
            >>> P2.history = ['D', 'D', 'D']
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.calculate_scores(P1, P2)
            (12, 12)
        """
        s1, s2 = 0, 0
        for pair in zip(p1.history, p2.history):
            if pair[0] == pair[1] == 'C':
                s1 += 2
                s2 += 2
            if pair[0] == pair[1] == 'D':
                s1 += 4
                s2 += 4
            if pair[0] == 'C' and pair[1] == 'D':
                s1 += 5
                s2 += 0
            if pair[0] == 'D' and pair[1] == 'C':
                s1 += 0
                s2 += 5
        return s1, s2


class Player:
    """
    A class for a player
    """
    def __init__(self):
        """
        Initiates an empty history and 0 score for every player

            >>> P1 = Player()
            >>> P1.history
            []
            >>> P1.score
            0
        """
        self.history = []
        self.score = 0

    def play(self, opponent):
        """
        This pits two players against each other: note that this will raise
        an error if no strategy method is defined (which are defined through
        class inheritance).

            >>> P1, P2 = Player(), Player()
            >>> P1.play(P2)
            Traceback (most recent call last):
            ...
            AttributeError: Player instance has no attribute 'strategy'

        Also note that it does not matter which player plays the other:

            >>> P2.play(P1)
            Traceback (most recent call last):
            ...
            AttributeError: Player instance has no attribute 'strategy'
        """
        s1, s2 = self.strategy(opponent), opponent.strategy(self)
        self.history.append(s1)
        opponent.history.append(s2)
