import random

from axelrod import Player


class Defector(Player):
    """
    A player who only ever defects
    """
    def strategy(self, opponent):
        """
        Always returns 'D'
        """
        return 'D'

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Defector'

class TrickyDefector(Player):
    """A defector that is trying to be tricky"""

    def strategy(self, opponent):
        """
        Almost always defects, but will try to trick the opponent into cooperating,
        namely if opponent has cooperated at least once in the past and has defected
        for the last 3 turns.
        """
        if 'C' in opponent.history and opponent.history[-3:] == ['D']*3:
            return 'C'
        return 'D'

    def __repr__(self):
        return "Tricky Defector"