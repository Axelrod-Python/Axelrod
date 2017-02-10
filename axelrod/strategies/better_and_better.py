from axelrod.actions import Actions
from axelrod.player import Player
from axelrod.random_ import random_choice
from axelrod.actions import Action

C, D = Actions.C, Actions.D


class BetterAndBetter(Player):
    """
    Defects with probability of '(1000 - current turn) / 1000'.
    Therefore it is less and less likely to defect as the round goes on.

    Names:
        - Better and Better: [PRISON1998]_

    """

    name = 'Better and Better'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        current_round = len(self.history) + 1
        probability = current_round / 1000
        return random_choice(probability)
