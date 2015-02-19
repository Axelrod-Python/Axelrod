from axelrod import Player

class Grudger(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected
    """
    def strategy(self, opponent):
        """
        Begins by playing C, then plays D for the remaining rounds if the opponent ever plays D
        """
        if 'D' in opponent.history:
            return 'D'
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Grudger'
