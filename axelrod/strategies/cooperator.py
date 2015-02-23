from axelrod import Player

class Cooperator(Player):
    """
    A player who only ever cooperates
    """
    def strategy(self, opponent):
        """
        Always returns 'C'
        """
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Cooperator'

class TrickyCooperator(Player):
    """A cooperator that is trying to be tricky"""

    def strategy(self, opponent):
        """
        Almost always cooperates, but will try to trick the opponent by defecting
        once in a while in order to get a better payout, namely if the opponent
        has not defected in the last ten turns and cooperated during last 3 turns.
        """
        if 'D' not in opponent.history[-10:] and opponent.history[-3:] == ['C']*3:
            return 'D'
        return 'C'

    def __repr__(self):
        return "Tricky Cooperator"
        