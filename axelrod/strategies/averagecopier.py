
from axelrod import Player, random_choice
import random



class AverageCopier(Player):
    """
    The player will cooperate with probability p if the opponent's cooperation ratio is p.
    Starts with random decision.
    """

    name = 'Average Copier'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        if len(opponent.history) == 0:
            # Randomly picks a strategy (not affected by history).
            return random_choice(0.5)
        p = opponent.cooperations // len(opponent.history)
        return random_choice(p)


class NiceAverageCopier(Player):
    """Same as Average Copier, but always starts by cooperating."""

    name = 'Nice Average Copier'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        if len(opponent.history) == 0:
            return 'C'
        p = opponent.cooperations // len(opponent.history)
        return random_choice(p)
