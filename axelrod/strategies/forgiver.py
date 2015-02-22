from axelrod import Player

class Forgiver(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected more than 10 percent of the time
    """
    def strategy(self, opponent):
        """
        Begins by playing C, then plays D if the opponent has defected more than 10 percent of the time
        """
        try:
            if opponent.history.count('D')>len(opponent.history)/10:
                return 'D'
            return 'C'
        except IndexError:
            return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Forgiver'
