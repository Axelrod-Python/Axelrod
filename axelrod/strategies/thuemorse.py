from axelrod import Actions, Player

class ThueMorse(Player):
    """A player who cooperates or defects according to the Thue-Morse sequence."""

    name = 'ThueMorse'
    classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def thuemorse_sequence(self, round_number):
        """The recursive definition of the Thue-Morse sequence"""
        if round_number == 0:
            return 0
        if round_number % 2 == 0:
            return self.thuemorse_sequence(round_number/2)
        if round_number % 2 == 1:
            return 1 - self.thuemorse_sequence((round_number - 1) / 2)

    def strategy(self, opponent):
        n = len(self.history) # Finds what round we are on
        if self.thuemorse_sequence(n) == 1:
            return Actions.C
        return Actions.D




class ThueMorseInverse(ThueMorse):
    """A player who defects or cooperates according to the Thue-Morse sequence (Inverse of ThueMorse)."""

    name = 'ThueMorseInverse'
    classifier = {
        'memory_depth': float('Inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        n = len(self.history) # Find what round we are on
        if self.thuemorse_sequence(n) == 1:
            return Actions.D
        return Actions.C
