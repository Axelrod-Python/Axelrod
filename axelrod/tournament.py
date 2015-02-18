"""
Recreate Axelrod's tournament


"""
import itertools
import random

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
        Initiate a tournament of players:

            >>> P1 = Defector()
            >>> P2 = Defector()
            >>> P3 = Defector()
            >>> axelrod = Axelrod(P1, P2, P3)
            >>> axelrod.players
            [Defector, Defector, Defector]
        """
        self.players = list(args)

    def round_robin(self, turns=200):
        """
        Plays a round robin where each match lasts turns.

        Defector viciously punishes Cooperator:

            >>> P1 = Defector()
            >>> P2 = Cooperator()
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.round_robin(turns=10)
            >>> for player in sorted(axelrod.players, key=lambda x: x.score):
            ...     print player, player.score
            Defector 0
            Cooperator 50

        Defector does very well against Tit for Tat:

            >>> P1 = Defector()
            >>> P2 = TitForTat()
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.round_robin(turns=10)
            >>> for player in sorted(axelrod.players, key=lambda x: x.score):
            ...     print player, player.score
            Defector 36
            Tit For Tat 41

        Cooperator does very well WITH Tit for Tat:

            >>> P1 = Cooperator()
            >>> P2 = TitForTat()
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.round_robin(turns=10)
            >>> for player in sorted(axelrod.players, key=lambda x: x.score):
            ...     print player, player.score
            Cooperator 20
            Tit For Tat 20

        Automatically runs all results as required for games with more players, taking
        the random player out:

            >>> P1 = Defector()
            >>> P2 = Cooperator()
            >>> P3 = TitForTat()
            >>> axelrod = Axelrod(P1, P2, P3)
            >>> axelrod.round_robin(turns=200)
            >>> for player in sorted(axelrod.players, key=lambda x: x.score):
            ...     print player, player.score
            Defector 796
            Tit For Tat 1201
            Cooperator 1400

        We see here that Tit for Tat does very poorly (compared to the Defector)
        despite the well known results. Why is this? Let us introduce another
        'aggressive' strategy

            >>> P1 = Defector()
            >>> P2 = Cooperator()
            >>> P3 = TitForTat()
            >>> P4 = Grudger()
            >>> axelrod = Axelrod(P1, P2, P3, P4)
            >>> axelrod.round_robin(turns=200)
            >>> for player in sorted(axelrod.players, key=lambda x: x.score):
            ...     print player, player.score
            Defector 1592
            Tit For Tat 1601
            Grudger 1601
            Cooperator 1800

        We see that Tit for Tat is much closer. Let us add in another strategy.

            >>> P1 = Defector()
            >>> P2 = Cooperator()
            >>> P3 = TitForTat()
            >>> P4 = Grudger()
            >>> P5 = GoByMajority()
            >>> axelrod = Axelrod(P1, P2, P3, P4, P5)
            >>> axelrod.round_robin(turns=200)
            >>> for player in sorted(axelrod.players, key=lambda x: x.score):
            ...     print player, player.score
            Tit For Tat 2001
            Grudger 2001
            Go By Majority 2001
            Cooperator 2200
            Defector 2388

        Now Tit for Tat is top of the pile and in fact the defector is at the bottom.
        Take a look at the various strategies.
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

            >>> random.seed(1)
            >>> P1 = Defector()
            >>> P2 = Cooperator()
            >>> P3 = TitForTat()
            >>> P4 = Grudger()
            >>> P5 = GoByMajority()
            >>> P6 = Random()
            >>> axelrod = Axelrod(P1, P2, P3, P4, P5, P6)
            >>> results = axelrod.tournament(turns=200, repetitions=10)
            >>> type(results)
            <type 'dict'>
            >>> for player in sorted(results.keys()):
            ...     print player, results[player]
            Grudger [2414, 4788, 7230, 9652, 12108, 14510, 16912, 19316, 21726, 24132]
            Defector [2784, 5572, 8340, 11104, 13924, 16684, 19468, 22204, 24960, 27720]
            Go By Majority [2457, 5114, 7583, 10262, 12688, 15135, 17713, 20365, 22898, 25558]
            Cooperator [2888, 5797, 8724, 11618, 14461, 17400, 20327, 23212, 26103, 29003]
            Tit For Tat [2584, 5143, 7681, 10223, 12746, 15297, 17849, 20400, 22946, 25505]
            Random [3456, 6282, 9600, 12370, 15762, 19125, 22192, 24999, 28129, 30918]

        Let us take a look at the min, mean and max of the results:
            >>> for player in sorted(results.keys()):
            ...     print player, min(results[player]), sum(results[player]) / float(10), max(results[player])
            Grudger 2414 13278.8 24132
            Defector 2784 15276.0 27720
            Go By Majority 2457 13977.3 25558
            Cooperator 2888 15953.3 29003
            Tit For Tat 2584 14037.4 25505
            Random 3456 17283.3 30918

        We get a similar conclusion to before with Grudger, Defect and Tit for Tat doing very well: in other words we see that cooperation is rewarded.
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

            >>> P1 = Defector()
            >>> P1.history = ['C', 'D']
            >>> P1.history
            ['C', 'D']
            >>> P2 = Cooperator()
            >>> P2.history = ['D', 'D']
            >>> P2.history
            ['D', 'D']
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.reset_player_history()
            >>> P1.history
            []
            >>> P2.history
            []
        """
        for player in self.players:
            player.history = []

    def reset_player_scores(self):
        """
        Resets all the player histories

            >>> P1 = Defector()
            >>> P1.score = 78
            >>> P1.score
            78
            >>> P2 = Cooperator()
            >>> P2.score = 55
            >>> P2.score
            55
            >>> axelrod = Axelrod(P1, P2)
            >>> axelrod.reset_player_scores()
            >>> P1.score
            0
            >>> P2.score
            0
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
