from axelrod import Actions, Player, init_args, random_choice

import random

C, D = Actions.C, Actions.D


class Prober(Player):
    """
    Plays D, C, C initially. Defects forever if opponent cooperated in moves 2
    and 3. Otherwise plays TFT.
    """

    name = 'Prober'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn == 2:
            return C
        if turn > 2:
            if opponent.history[1: 3] == [C, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober2(Player):
    """
    Plays D, C, C initially. Cooperates forever if opponent played D then C
    in moves 2 and 3. Otherwise plays TFT.
    """

    name = 'Prober 2'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn == 2:
            return C
        if turn > 2:
            if opponent.history[1: 3] == [D, C]:
                return C
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober3(Player):
    """
    Plays D, C initially. Defects forever if opponent played C in moves 2.
    Otherwise plays TFT.
    """

    name = 'Prober 3'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return C
        if turn > 1:
            if opponent.history[1] == C:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class Prober4(Player):
    """
    Plays C, C, D, C, D, D, D, C, C, D, C, D, C, C, D, C, D, D, C, D initially.
    Counts retaliating and provocative defections of the opponent.
    If the absolute difference between the counts is smaller or equal to 2,
    defects forever.
    Otherwise plays C for the next 5 turns and TFT for the rest of the game.

    Names:

    - prober4: [PRISON1998]_
    """

    name = 'Prober 4'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self):
        Player.__init__(self)
        self.init_sequence = [
            C, C, D, C, D, D, D, C, C, D, C, D, C, C, D, C, D, D, C, D
        ]
        self.just_Ds = 0
        self.unjust_Ds = 0
        self.turned_defector = False

    def strategy(self, opponent):
        if not self.history:
            return self.init_sequence[0]
        turn = len(self.history)
        if turn < len(self.init_sequence):
            if opponent.history[-1] == D:
                if self.history[-1] == D:
                    self.just_Ds += 1
                if self.history[-1] == C:
                    self.unjust_Ds += 1
            return self.init_sequence[turn]
        if turn == len(self.init_sequence):
            diff_in_Ds = abs(self.just_Ds - self.unjust_Ds)
            self.turned_defector = (diff_in_Ds <= 2)
        if self.turned_defector:
            return D
        if not self.turned_defector:
            if turn < len(self.init_sequence) + 5:
                return C
            return D if opponent.history[-1] == D else C

    def reset(self):
        Player.reset(self)
        self.just_Ds = 0
        self.unjust_Ds = 0
        self.turned_defector = False


class HardProber(Player):
    """
    Plays D, D, C, C initially. Defects forever if opponent cooperated in moves
    2 and 3. Otherwise plays TFT.
    """

    name = 'Hard Prober'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),  # Long memory
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        turn = len(self.history)
        if turn == 0:
            return D
        if turn == 1:
            return D
        if turn == 2:
            return C
        if turn == 3:
            return C
        if turn > 3:
            if opponent.history[1: 3] == [C, C]:
                return D
            else:
                # TFT
                return D if opponent.history[-1:] == [D] else C


class NaiveProber(Player):
    """
    Like tit-for-tat, but it occasionally defects with a small probability.

    For reference see: "Engineering Design of Strategies for Winning
    Iterated Prisoner's Dilemma Competitions" by Jiawei Li, Philip Hingston,
    and Graham Kendall.  IEEE TRANSACTIONS ON COMPUTATIONAL INTELLIGENCE AND AI
    IN GAMES, VOL. 3, NO. 4, DECEMBER 2011
    """

    name = 'Naive Prober'
    classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, p=0.1):
        """
        Parameters
        ----------
        p, float
            The probability to defect randomly
        """
        Player.__init__(self)
        self.p = p
        if (self.p == 0) or (self.p == 1):
            self.classifier['stochastic'] = False

    def strategy(self, opponent):
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            return D
        # Otherwise cooperate, defect with probability 1 - self.p
        choice = random_choice(1 - self.p)
        return choice

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))


class RemorsefulProber(NaiveProber):
    """
    Like Naive Prober, but it remembers if the opponent responds to a random
    defection with a defection by being remorseful and cooperating.

    For reference see: "Engineering Design of Strategies for Winning
    Iterated Prisoner's Dilemma Competitions" by Jiawei Li, Philip Hingston,
    and Graham Kendall.  IEEE TRANSACTIONS ON COMPUTATIONAL INTELLIGENCE AND AI
    IN GAMES, VOL. 3, NO. 4, DECEMBER 2011

    A more complete description is given in "The Selfish Gene"
    (https://books.google.co.uk/books?id=ekonDAAAQBAJ):

    "Remorseful Prober remembers whether it has just spontaneously defected, and
    whether the result was prompt retaliation. If so, it 'remorsefully' allows
    its opponent 'one free hit' without retaliating."
    """

    name = 'Remorseful Prober'
    classifier = {
        'memory_depth': 2,  # It remembers if its previous move was random
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, p=0.1):
        NaiveProber.__init__(self, p)
        self.probing = False

    def strategy(self, opponent):
        # First move
        if len(self.history) == 0:
            return C
        # React to the opponent's last move
        if opponent.history[-1] == D:
            if self.probing:
                self.probing = False
                return C
            return D

        # Otherwise cooperate with probability 1 - self.p
        if random.random() < 1 - self.p:
            self.probing = False
            return C

        self.probing = True
        return D

    def reset(self):
        Player.reset(self)
        self.probing = False
