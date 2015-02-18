from axelrod import Player

class Grudger(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected
    """
    def strategy(self, opponent):
        """
        """
        if 'D' in opponent.history:
            return 'D'
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Grudger'
