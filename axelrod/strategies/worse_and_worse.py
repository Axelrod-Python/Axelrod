import random

from axelrod import Actions, Player, random_choice

C, D = Actions.C, Actions.D

class WorseAndWorse (Player):
    """
    Defects with probability of 'current turn / 1000'. Therefore
    it is more and more likely to defect as the round goes on.

    Names:
        - worse_and_worse: [PRISON1998]

    """

    name = 'Worse and worse'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        current_round = len(self.history) + 1
        if random.randint(0, 1000) < current_round:
            return D
        return C


class WorseAndWorseRandom (Player):
    """
    This strategy is based of 'Worse And Worse' but will defect with probability
    of 'current turn / total no. of turns'.

    """

    name = 'Worse and worse random'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent):
        current_round = len(self.history) + 1
        expected_length = self.match_attributes['length']
        probability = 1 - float(current_round) / expected_length
        return random_choice(probability)
