from axelrod import Player
import random


class Random(Player):
    """A player who randomly chooses between cooperating and defecting."""

    name = 'Random'
    behaviour = {
        'memory_depth': 0,  # Memory-one Four-Vector = (p, p, p, p)
        'stochastic': True,
        'inspects_opponent_source': False,
        'manipulates_opponent_source': False,
        'manipulates_opponent_state': False
    }

    def __init__(self, p=0.5):
        Player.__init__(self)
        self.p = p

    def strategy(self, opponent):
        r = random.random()
        if r > self.p:
            return 'D'
        return 'C'

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))
