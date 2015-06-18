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

    def __init__(self, rounds_to_cooperate=10):
        Player.__init__(self)
        self._rounds_to_cooperate = rounds_to_cooperate

    def strategy(self, opponent):
        rounds = self._rounds_to_cooperate
        if len(self.history) < rounds:
            return 'C'
        cooperate_count = opponent.history[-rounds:].count('C')
        prop_cooperate = cooperate_count / float(rounds)
        prob_cooperate = max(0, prop_cooperate - 0.10)
        r = random.random()
        if r < prob_cooperate:
            return 'C'
        return 'D'


class Feld(Player):
    """
    Defects when opponent defects. Cooperates with a probability that decreases
    to 0.5 at round 200.
    """

    name = "Feld"
    memoryone = False # Probabilities are not constant

    def __init__(self, start_coop_prob=1.0, end_coop_prob=0.5, rounds_of_decay=200):
        Player.__init__(self)
        self._start_coop_prob = start_coop_prob
        self._end_coop_prob = end_coop_prob
        self._rounds_of_decay = rounds_of_decay

    def _cooperation_probability(self):
        """It's not clear what the interpolating function is, so we'll do
        something simple that decreases monotonically from 1.0 to 0.5 over
        200 rounds."""
        slope = (self._end_coop_prob - self._start_coop_prob ) / float(self._rounds_of_decay)
        rounds = len(self.history)
        return max(self._start_coop_prob + slope * rounds,
                   self._end_coop_prob)

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
