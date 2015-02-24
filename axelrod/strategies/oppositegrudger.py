from axelrod import Player

class OppositeGrudger(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected
    """

    name = 'Opposite Grudger'

    def strategy(self, opponent):
        """
        Begins by playing D, then plays C for the remaining rounds if the opponent ever plays C
        """
        if 'C' in opponent.history:
            return 'C'
        return 'D'
