from axelrod import Player

class Defector(Player):
    """
    A player who only ever defects
    """
    def strategy(self, opponent):
        """
        Always returns 'D'
        """
        return 'D'

    def __repr__(self):
        """
i       The string method for the strategy:
        """
        return 'Defector'
