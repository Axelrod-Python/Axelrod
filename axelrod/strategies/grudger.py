from axelrod import Player


class Grudger(Player):
    """A player starts by cooperating however will defect if at any point the opponent has defected."""

    name = 'Grudger'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """Begins by playing C, then plays D for the remaining rounds if the opponent ever plays D."""
        if opponent.defections:
            return 'D'
        return 'C'


class ForgetfulGrudger(Player):
    """A player starts by cooperating however will defect if at any point the
    opponent has defected, but forgets after mem_length matches."""

    name = 'Forgetful Grudger'
    classifier = {
        'memory_depth': 10,
        'stochastic': False,
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
            return 'D'
        elif 'D' in opponent.history[-1:]:
            self.grudged = True
            return 'D'
        return 'C'

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """Begins by playing D, then plays C for the remaining rounds if the opponent ever plays C."""
        if opponent.cooperations:
            return 'C'
        return 'D'


class Aggravater(Player):
    """Grudger, except that it defects on the first 3 turns"""

    name = 'Aggravater'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        if len(opponent.history) < 3:
            return 'D'
        elif opponent.defections:
            return 'D'
        return 'C'
