from axelrod import Actions, Player
from random import randint

class WorseAndWorse (Player):
    """
    Defects with probability of 'current turn / total no. of turns'. Therefore it
    is more and more likely to defect as the round goes on.

    Names

    - worse_and_worse: [PRISON1998]

    """

    name = 'Worse and worse'
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
        expected_length = self.match_attributes['length']
        if randint(0, expected_length) < (len(self.history) + 1):
            return Actions.D
        return Actions.C
