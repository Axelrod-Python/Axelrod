from axelrod import Player

class TitForTat(Player):
    """
    A player starts by cooperating and then mimics previous move by opponent.
    """
    def strategy(self, opponent):
        """
        Begins by playing 'C':

            >>> random.seed(1)
            >>> P1 = TitForTat()
            >>> P2 = Player()
            >>> P1.strategy(P2)
            'C'

        This is affected by the history of the opponent:

            >>> P1.history = ['C', 'D', 'C']
            >>> P2.history = ['C', 'C', 'D']
            >>> P1.strategy(P2)
            'D'

            >>> P1.history.append('D')
            >>> P2.history.append('C')
            >>> P1.strategy(P2)
            'C'
        >>>
        """
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

    def __repr__(self):
        """
i       The string method for the strategy:

            >>> P1 = Cooperator()
            >>> print P1
            Cooperator
        """
        return 'Tit For Tat'
