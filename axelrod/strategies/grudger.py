from axelrod import Player

class Grudger(Player):
    """
    A player starts by cooperating however will defect if at any point the opponent has defected
    """
    def strategy(self, opponent):
        """
        Begins by playing 'C':

            >>> P1 = Grudger()
            >>> P2 = Player()
            >>> P1.strategy(P2)
            'C'

        This is affected by the history of the opponent:

            >>> P1.history = ['C', 'C', 'C']
            >>> P2.history = ['C', 'C', 'C']
            >>> P1.strategy(P2)
            'C'

        If at any point the opponent defects then the player will forever defect:

            >>> P1.history = ['C', 'C', 'D', 'D', 'D']
            >>> P2.history = ['C', 'D', 'C', 'C', 'C']
            >>> P1.strategy(P2)
            'D'
        >>>
        """
        if 'D' in opponent.history:
            return 'D'
        return 'C'

    def __repr__(self):
        """
i       The string method for the strategy:

            >>> P1 = Grudger()
            >>> print P1
            Grudger
        """
        return 'Grudger'
