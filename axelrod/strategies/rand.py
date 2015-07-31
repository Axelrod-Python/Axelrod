from axelrod import Player
import random


class Random(Player):
    """A player who randomly chooses between cooperating and defecting."""

    name = 'Random'
    memory_depth = 0  # Memory-one Four-Vector = (p, p, p, p)

    def __init__(self, p=0.5):
        Player.__init__(self)
        self.p = p

    def strategy(self, opponent):
        r = random.random()
        if r > self.p:
            return 'D'
        return 'C'
