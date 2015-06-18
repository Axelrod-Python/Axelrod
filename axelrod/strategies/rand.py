from collections import Counter

from axelrod import Player
import random


class Random(Player):
    """A player who randomly chooses between cooperating and defecting."""

    name = 'Random'
    memoryone = True  # Four-Vector = (0.5, 0.5, 0.5, 0.5)

    def strategy(self, opponent):
        return random.choice(['C', 'D'])


class Tullock(Player):
    """
    Cooperates for the first 11 rounds then randomly cooperates 10% less often
    than the opponent has in previous rounds."""

    name = "Tullock"
    memoryone = False # memory-10

    def strategy(self, opponent):
        if len(self.history) < 11:
            return 'C'
        counter = Counter(opponent.history[-10:])
        prop_cooperate = counter['C'] / 10.
        prob_cooperate = max(0, prop_cooperate - 0.10)
        r = random.random()
        if r < prop_cooperate:
            return 'C'
        return 'D'

class Feld(Player):
    """
    Defects when opponent defects. Cooperates with a probability that decreases
    to 0.5 at round 200.
    """

    name = "Feld"
    memoryone = False # Probabilities are not constant

    def _cooperation_probability(self):
        """It's not clear what the interpolating function is, so we'll do
        something simple that decreases monotonically from 1.0 to 0.5 over
        200 rounds."""
        slope = 0.5/200
        rounds = len(self.history)
        return max(1.0 - slope * rounds, 0.5)

    def strategy(self, opponent):
        if not self.history:
            return 'C'
        if opponent.history[-1] == 'D':
            return 'D'
        p = self._cooperation_probability()
        r = random.random()
        if r < p:
            return 'C'
        return 'D'
