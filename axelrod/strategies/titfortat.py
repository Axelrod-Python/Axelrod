from axelrod import Player

class TitForTat(Player):
    """
    A player starts by cooperating and then mimics previous move by opponent.
    """
    def strategy(self, opponent):
        """
        Begins by playing 'C':
        This is affected by the history of the opponent: the strategy simply repeats the last action of the opponent
        """
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Tit For Tat'
