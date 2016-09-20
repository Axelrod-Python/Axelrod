from axelrod import Actions, Player

C, D = Actions.C, Actions.D

class Grudger(Player):
    """
    A player starts by cooperating however will defect if at any point the
    opponent has defected.

    Names:

    - Friedman's strategy: [Axelrod1980]_
    - Grudger: [Li2011]_
    - Grim: [Berg2015]_
    - Grim Trigger: [Banks1980]_
    """

    name = 'Grudger'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        """Begins by playing C, then plays D for the remaining rounds if the opponent ever plays D."""
        if opponent.defections:
            return D
        return C


class ForgetfulGrudger(Player):
    """A player starts by cooperating however will defect if at any point the
    opponent has defected, but forgets after mem_length matches."""

    name = 'Forgetful Grudger'
    classifier = {
        'memory_depth': 10,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        """Initialised the player."""
        super(ForgetfulGrudger, self).__init__()
        self.mem_length = 10
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent):
        """Begins by playing C, then plays D for mem_length rounds if the opponent ever plays D."""
        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if self.grudged:
            self.grudge_memory += 1
            return D
        elif D in opponent.history[-1:]:
            self.grudged = True
            return D
        return C

    def reset(self):
        """Resets scores and history."""
        Player.reset(self)
        self.grudged = False
        self.grudge_memory = 0


class OppositeGrudger(Player):
    """A player starts by defecting however will cooperate if at any point the opponent has cooperated."""

    name = 'Opposite Grudger'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        """Begins by playing D, then plays C for the remaining rounds if the opponent ever plays C."""
        if opponent.cooperations:
            return C
        return D


class Aggravater(Player):
    """Grudger, except that it defects on the first 3 turns"""

    name = 'Aggravater'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        if len(opponent.history) < 3:
            return D
        elif opponent.defections:
            return D
        return C


class SoftGrudger(Player):
    """
    A modification of the Grudger strategy. Instead of punishing by always
    defecting: punishes by playing: D, D, D, D, C, C. (Will continue to
    cooperate afterwards).

    For reference see: "Engineering Design of Strategies for Winning
    Iterated Prisoner's Dilemma Competitions" by Jiawei Li, Philip Hingston,
    and Graham Kendall.  IEEE TRANSACTIONS ON COMPUTATIONAL INTELLIGENCE AND AI
    IN GAMES, VOL. 3, NO. 4, DECEMBER 2011
    """

    name = 'Soft Grudger'
    classifier = {
        'memory_depth': 6,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        """Initialised the player."""
        super(SoftGrudger, self).__init__()
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent):
        """Begins by playing C, then plays D, D, D, D, C, C against a defection
        """
        if self.grudged:
            strategy = [D, D, D, C, C][self.grudge_memory]
            self.grudge_memory += 1
            if self.grudge_memory == 5:
                self.grudge_memory = 0
                self.grudged = False
            return strategy
        elif D in opponent.history[-1:]:
            self.grudged = True
            return D
        return C

    def reset(self):
        """Resets scores and history."""
        Player.reset(self)
        self.grudged = False
        self.grudge_memory = 0



class GrudgerAlternator(Player):
    """
    A player starts by cooperating until the first opponents defection,
    then alternates D-C.

    Names:

    - c_then_per_dc: [PRISON1998]_
    - Grudger Alternator: Original name by Geraint Palmer
    """

    name = 'GrudgerAlternator'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """Begins by playing C, then plays Alternator for the remaining rounds if the opponent ever plays D."""
        if opponent.defections:
            if self.history[-1] == Actions.C:
                return Actions.D
        return Actions.C



class EasyGo(Player):
    """
    A player starts by defecting however will cooperate if at any point the opponent has defected.

    Names:

    - Easy Go [PRISON1998]_
    """

    name = 'EasyGo'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        """Begins by playing D, then plays C for the remaining rounds if the opponent ever plays D."""
        if opponent.defections:
            return C
        return D
