from axelrod import Player

class Alternator(Player):
    """
    A player who alternates between cooperating and defecting
    """

    name = 'Alternator'

    def strategy(self, opponent):
        """
        Alternate 'C' and 'D'
        """
        if len(self.history) == 0:
            return 'C'
        if self.history[-1] == 'C':
            return 'D'
        return 'C'
