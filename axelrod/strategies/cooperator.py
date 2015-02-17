from axelrod import Player

class Cooperator(Player):
    """
    A player who only ever cooperates
    """
    def strategy(self, opponent):
        """
        Always returns 'C'

            >>> P1 = Cooperator()
            >>> P2 = Player()
            >>> P1.strategy(P2)
            'C'

        This is not affect by the history of either player:

            >>> P1.history = ['C', 'D', 'C']
            >>> P2.history  = ['C', 'C', 'D']
            >>> P1.strategy(P2)
            'C'
        >>>
        """
        return 'C'

    def __repr__(self):
        """
i       The string method for the strategy:

            >>> P1 = Cooperator()
            >>> print P1
            Cooperator
        """
        return 'Cooperator'
