"""
Additional strategies from Axelrod's two tournaments.
"""

import random

from axelrod import Player
from.memoryone import MemoryOnePlayer


flip_dict = {'C': 'D', 'D': 'C'}


## First Tournament

class Davis(Player):
    """A player starts by cooperating for 10 rounds then plays Grudger,
    defecting if at any point the opponent has defected."""

    name = 'Davis'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, rounds_to_cooperate=10):
        Player.__init__(self)
        self._rounds_to_cooperate = rounds_to_cooperate
        self.init_args = (self._rounds_to_cooperate,)

    def strategy(self, opponent):
        """Begins by playing C, then plays D for the remaining rounds if the
        opponent ever plays D."""
        if len(self.history) < self._rounds_to_cooperate:
            return 'C'
        if opponent.defections:
            return 'D'
        return 'C'


class Feld(Player):
    """
    Defects when opponent defects. Cooperates with a probability that decreases
    to 0.5 at round 200.
    """

    name = "Feld"
    classifier = {
        'memory_depth': 200, # Varies actually, eventually becomes depth 1
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, start_coop_prob=1.0, end_coop_prob=0.5,
                 rounds_of_decay=200):
        Player.__init__(self)
        self._start_coop_prob = start_coop_prob
        self._end_coop_prob = end_coop_prob
        self._rounds_of_decay = rounds_of_decay
        self.init_args = (start_coop_prob,
                          end_coop_prob,
                          rounds_of_decay)

    def _cooperation_probability(self):
        """It's not clear what the interpolating function is, so we'll do
        something simple that decreases monotonically from 1.0 to 0.5 over
        200 rounds."""
        diff = (self._end_coop_prob - self._start_coop_prob)
        slope = diff / float(self._rounds_of_decay)
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


class Grofman(MemoryOnePlayer):
    """
    Cooperates with probability 2/7.
    """

    name = "Grofman"

    def __init__(self):
        p = float(2) / 7
        four_vector = (p, p, p, p)
        super(self.__class__, self).__init__(four_vector)
        self.init_args = ()


class Joss(MemoryOnePlayer):
    """
    Cooperates with probability 0.9 when the opponent cooperates, otherwise
    emulates Tit-For-Tat.
    """

    name = "Joss"

    def __init__(self, p=0.9):
        four_vector = (p, 0, p, 0)
        self.p = p
        super(self.__class__, self).__init__(four_vector)
        self.init_args = (p,)

    def __repr__(self):
        return "%s: %s" % (self.name, round(self.p, 2))


class Shubik(Player):
    """
    Plays like Tit-For-Tat with the following modification. After
    each retaliation, the number of rounds that Shubik retaliates
    increases by 1.
    """

    name = 'Shubik'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        Player.__init__(self)
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0

    def _decrease_retaliation_counter(self):
        """Lower the remaining owed retaliation count and flip to non-retaliate
        if the count drops to zero."""
        if self.is_retaliating:
            self.retaliation_remaining -= 1
            if self.retaliation_remaining == 0:
                self.is_retaliating = False

    def strategy(self, opponent):
        if not opponent.history:
            return 'C'
        if opponent.history[-1] == 'D':
            # Retaliate against defections
            if self.history[-1] == 'C': # it's on now!
                # Lengthen the retaliation period
                self.is_retaliating = True
                self.retaliation_length += 1
                self.retaliation_remaining = self.retaliation_length
                self._decrease_retaliation_counter()
                return 'D'
            else:
                # Just retaliate
                if self.is_retaliating:
                    self._decrease_retaliation_counter()
                return 'D'
        if self.is_retaliating:
            # Are we retaliating still?
            self._decrease_retaliation_counter()
            return 'D'
        return 'C'

    def reset(self):
        Player.reset(self)
        self.is_retaliating = False
        self.retaliation_length = 0
        self.retaliation_remaining = 0


class Tullock(Player):
    """
    Cooperates for the first 11 rounds then randomly cooperates 10% less often
    than the opponent has in previous rounds."""

    name = "Tullock"
    classifier = {
        'memory_depth': 11, # long memory, modified by init
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, rounds_to_cooperate=11):
        Player.__init__(self)
        self._rounds_to_cooperate = rounds_to_cooperate
        self.__class__.memory_depth = rounds_to_cooperate
        self.init_args = (rounds_to_cooperate,)

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


## Second Tournament

class Champion(Player):
    """
    Strategy submitted to Axelrod's second tournament by Danny Champion.
    """

    name = "Champion"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        current_round = len(self.history)
        expected_length = self.tournament_attributes['length']
        # Cooperate for the first 1/20-th of the game
        if current_round == 0:
            return 'C'
        if current_round < expected_length / 20.:
            return 'C'
        # Mirror partner for the next phase
        if current_round < expected_length * 5 / 40.:
            return opponent.history[-1]
        # Now cooperate unless all of the necessary conditions are true
        defection_prop = float(opponent.defections) / len(opponent.history)
        if opponent.history[-1] == 'D':
            r = random.random()
            if defection_prop > max(0.4, r):
                return 'D'
        return 'C'


class Eatherley(Player):
    """
    Strategy submitted to Axelrod's second tournament by Graham Eatherley.
    """

    name = "Eatherley"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        # Cooperate on the first move
        if not len(self.history):
            return 'C'
        # Reciprocate cooperation
        if opponent.history[-1] == 'C':
            return 'C'
        # Respond to defections with probability equal to opponent's total
        # proportion of defections
        defection_prop = float(opponent.defections) / len(opponent.history)
        r = random.random()
        if r < defection_prop:
            return 'D'
        return 'C'


class Tester(Player):
    """
    Submitted to Axelrod's second tournament by David Gladstein.

    Defects on the first move and plays TFT if the opponent ever defects (after
    one apology cooperation round). Otherwise alternate cooperation and defection.
    """

    name = "Tester"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self):
        Player.__init__(self)
        self.is_TFT = False

    def strategy(self, opponent):
        # Defect on the first move
        if not opponent.history:
            return 'D'
        # Am I TFT?
        if self.is_TFT:
            return 'D' if opponent.history[-1:] == ['D'] else 'C'
        else:
            # Did opponent defect?
            if opponent.history[-1] == 'D':
                self.is_TFT = True
                return 'C'
            if len(self.history) in [1, 2]:
                return 'C'
            # Alternate C and D
            return flip_dict[self.history[-1]]

    def reset(self):
        Player.reset(self)
        self.is_TFT = False
