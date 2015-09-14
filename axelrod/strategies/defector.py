from axelrod import Player


class Defector(Player):
    """A player who only ever defects."""

    name = 'Defector'
    classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'D'


class TrickyDefector(Player):
    """A defector that is trying to be tricky."""

    name = "Tricky Defector"
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        """Almost always defects, but will try to trick the opponent into cooperating.

        Defect if opponent has cooperated at least once in the past and has defected
        for the last 3 turns in a row.
        """
        if 'C' in opponent.history and opponent.history[-3:] == ['D'] * 3:
            return 'C'
        return 'D'
