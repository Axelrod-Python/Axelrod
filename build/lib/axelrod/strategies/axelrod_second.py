"""
Additional strategies from Axelrod's second tournament.
"""

import random

from axelrod import Actions, Player, flip_action, random_choice

C, D = Actions.C, Actions.D


class Champion(Player):
    """
    Strategy submitted to Axelrod's second tournament by Danny Champion.
    """

    name = "Champion"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["length"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        current_round = len(self.history)
        expected_length = self.match_attributes['length']
        # Cooperate for the first 1/20-th of the game
        if current_round == 0:
            return C
        if current_round < expected_length / 20.:
            return C
        # Mirror partner for the next phase
        if current_round < expected_length * 5 / 40.:
            return opponent.history[-1]
        # Now cooperate unless all of the necessary conditions are true
        defection_prop = float(opponent.defections) / len(opponent.history)
        if opponent.history[-1] == D:
            r = random.random()
            if defection_prop > max(0.4, r):
                return D
        return C


class Eatherley(Player):
    """
    Strategy submitted to Axelrod's second tournament by Graham Eatherley.
    """

    name = "Eatherley"
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        # Cooperate on the first move
        if not len(opponent.history):
            return C
        # Reciprocate cooperation
        if opponent.history[-1] == C:
            return C
        # Respond to defections with probability equal to opponent's total
        # proportion of defections
        defection_prop = float(opponent.defections) / len(opponent.history)
        return random_choice(1 - defection_prop)


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
        'makes_use_of': set(),
        'long_run_time': False,
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
            return D
        # Am I TFT?
        if self.is_TFT:
            return D if opponent.history[-1:] == [D] else C
        else:
            # Did opponent defect?
            if opponent.history[-1] == D:
                self.is_TFT = True
                return C
            if len(self.history) in [1, 2]:
                return C
            # Alternate C and D
            return flip_action(self.history[-1])

    def reset(self):
        Player.reset(self)
        self.is_TFT = False
