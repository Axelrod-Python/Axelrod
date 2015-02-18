from axelrod import Player
import random

class Random(Player):
    """
    A player who randomly chooses between cooperating and defecting
    """
    def strategy(self, opponent):
        """
        Always returns 'C'

            >>> random.seed(1)
            >>> P1 = Random()
            >>> P2 = Player()
            >>> P1.strategy(P2)
            'C'

        This is not affect by the history of either player:

            >>> random.seed(1)
            >>> P1.history = ['C', 'D', 'C']
            >>> P2.history = ['C', 'C', 'D']
            >>> P1.strategy(P2)
            'C'

        It is simply a random choice:

            >>> random.seed(2)
            >>> P1.strategy(P2)
            'D'
            >>> P1.strategy(P2)
            'D'
            >>> P1.strategy(P2)
            'C'
        >>>
        """
        return random.choice(['C','D'])

    def __repr__(self):
        """
i       The string method for the strategy:

            >>> P1 = Cooperator()
            >>> print P1
            Cooperator
        """
        return 'Random'
