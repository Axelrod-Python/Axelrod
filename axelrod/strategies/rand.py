from axelrod import Player
import random

class Random(Player):
    """A player who randomly chooses between cooperating and defecting."""

    name = 'Random'
    memoryone = True # Four-Vector = (0.5, 0.5, 0.5, 0.5)

    def strategy(self, opponent):
        return random.choice(['C','D'])
