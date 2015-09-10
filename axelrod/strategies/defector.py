from axelrod import Player


class Defector(Player):
    """A player who only ever defects."""

    name = 'Defector'
    behaviour = {
        'memory_depth': 0,
        'stochastic': False,
        'inspects_opponent_source': False,
        'manipulates_opponent_source': False,
        'manipulates_opponent_state': False
    }

    @staticmethod
    def strategy(opponent):
        return 'D'


class TrickyDefector(Player):
    """A defector that is trying to be tricky."""

    name = "Tricky Defector"
    behaviour = {
        'memory_depth': float('inf')  # Long memory
    }

    def strategy(self, opponent):
        """Almost always defects, but will try to trick the opponent into cooperating.

        Defect if opponent has cooperated at least once in the past and has defected
        for the last 3 turns in a row.
        """
        if 'C' in opponent.history and opponent.history[-3:] == ['D'] * 3:
            return 'C'
        return 'D'
