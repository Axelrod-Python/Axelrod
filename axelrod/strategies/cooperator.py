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
