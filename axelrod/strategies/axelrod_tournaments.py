"""
Additional strategies from Axelrod's two tournaments.
"""

from axelrod import Player

import random


class Eatherley(Player):
    """
    Strategy submitted to Axelrod's second tournament by Graham Eatherley.
    """

    name = "Eatherley"
    memory_depth = float('inf')

    def strategy(self, opponent):
        # Cooperate on the first move
        if not len(self.history):
            return 'C'
        # Reciprocate cooperation
        if opponent.history[-1] == 'C':
            return 'C'
        # Respond to defections with probability equal to opponent's total
        # proportion of defections
        opponent_defections = len([x for x in opponent.history if x == 'D'])
        defection_prop = float(opponent_defections) / len(opponent.history)
        r = random.random()
        if r < defection_prop:
            return 'D'
        return 'C'


class Champion(Player):
    """
    Strategy submitted to Axelrod's second tournament by Danny Champion.
    """

    name = "Champion"
    memory_depth = float('inf')

    def __init__(self):
        Player.__init__(self)
        self.rounds = 200

    def strategy(self, opponent):
        current_round = len(self.history)
        expected_length = self.rounds # how are we getting this?
        # Cooperate for the first 1/20-th of the game
        if current_round < expected_length / 20.:
            return 'C'
        # Mirror partner for the next phase
        if current_round < expected_length * 5 / 40.:
            return opponent.history[-1]
        # Now cooperate unless all of the necessary conditions are true
        opponent_defections = len([x for x in opponent.history if x == 'D'])
        defection_prop = float(opponent_defections) / len(opponent.history)
        if opponent.history[-1] == 'D':
            r = random.random()
            if defection_prop > max(0.4, r):
                return 'D'
        return 'C'
