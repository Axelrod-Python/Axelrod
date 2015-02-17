from axelrod import Player

class GoByMajority(Player):
    """
    A player examines the history of the opponent: if the opponent has more defections than cooperations then the player defects
    """
    def strategy(self, opponent):
        """
        Begins by playing 'C':

            >>> P1 = GoByMajority()
            >>> P2 = Player()
            >>> P1.strategy(P2)
            'C'

        This is affected by the history of the opponent:

            >>> P1.history = ['C', 'C', 'C']
            >>> P2.history = ['C', 'C', 'C']
            >>> P1.strategy(P2)
            'C'

        As long as the opponent cooperates at least as often as they defect then the player will defect.

            >>> P1.history = ['C', 'D', 'D', 'D']
            >>> P2.history = ['D', 'D', 'C', 'C']
            >>> P1.strategy(P2)
            'C'

        If at any point the opponent has more defections than cooperations the player defects.

            >>> P1.history = ['C', 'C', 'D', 'D', 'D']
            >>> P2.history = ['C', 'D', 'D', 'D', 'C']
            >>> P1.strategy(P2)
            'D'
        >>>
        """
        if sum([s == 'D' for s in opponent.history]) > sum([s == 'C' for s in opponent.history]):
            return 'D'
        return 'C'

    def __repr__(self):
        """
i       The string method for the strategy:

            >>> P1 = GoByMajority()
            >>> print P1
            Go By Majority
        """
        return 'Go By Majority'
