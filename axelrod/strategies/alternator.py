from axelrod import Player

class Alternator(Player):
    """
    A player who alternates between cooperating and defecting
    """
    def strategy(self, opponent):
        """
        Alternate 'C' and 'D'
        """
        if len(self.history) == 0:
            return 'C'
        if self.history[-1] == 'C':
            return 'D'
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Alternator'
