from axelrod import Player

class Defector(Player):
    """
    A player who only ever defects
    """
    def strategy(self, opponent):
        """
        Always returns 'D'

            >>> P1 = Defector()
            >>> P2 = Player()
            >>> P1.strategy(P2)
            'D'

        This is not affect by the history of either player:

            >>> P1.history = ['C', 'D', 'C']
            >>> P2  = ['C', 'C', 'D']
            >>> P1.strategy(P2)
            'D'
        >>>
        """
        return 'D'

    def __repr__(self):
        """
i       The string method for the strategy:

            >>> P1 = Defector()
            >>> print P1
            Defector
        """
        return 'Defector'
