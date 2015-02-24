from axelrod import Player
import random

class Random(Player):
    """
    A player who randomly chooses between cooperating and defecting
    """

    name = 'Random'

    def strategy(self, opponent):
        """
        Randomly picks a strategy (not affected by history)
        """
        return random.choice(['C','D'])
