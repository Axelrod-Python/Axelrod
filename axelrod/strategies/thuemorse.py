from axelrod import Actions, Player

class ThueMorse(Player):
    """
    A player who cooperates or defects according to the Thue-Morse sequence.

    The first few terms of the Thue-Morse sequence are:::
    0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0 . . .
    """

    name = 'ThueMorse'
    round_number = 0
    classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def thuemorse_sequence(self, n):
        """The recursive definition of the Thue-Morse sequence"""
        if n == 0:
            return 0
        if n % 2 == 0:
            return self.thuemorse_sequence(n/2)
        if n % 2 == 1:
            return 1 - self.thuemorse_sequence((n - 1) / 2)

    def strategy(self, opponent):
        ThMo = self.thuemorse_sequence(self.round_number)
        self.round_number += 1
        if ThMo == 1:
            return Actions.C
        return Actions.D




class ThueMorseInverse(ThueMorse):
    """A player who defects or cooperates according to the Thue-Morse sequence (Inverse of ThueMorse)."""

    name = 'ThueMorseInverse'
    round_number = 0
    classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        ThMo = self.thuemorse_sequence(self.round_number)
        self.round_number += 1
        if ThMo == 1:
            return Actions.D
        return Actions.C
