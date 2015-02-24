from axelrod import Player
import random

class Random(Player):
    """A player who randomly chooses between cooperating and defecting."""

    name = 'Random'

    def strategy(self, opponent):
        return random.choice(['C','D'])
