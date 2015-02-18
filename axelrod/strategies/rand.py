from axelrod import Player
import random

class Random(Player):
    """
    A player who randomly chooses between cooperating and defecting
    """
    def strategy(self, opponent):
        """
        Randomly picks a strategy (not affected by history)
        """
        return random.choice(['C','D'])

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Random'
