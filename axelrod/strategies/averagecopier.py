
from axelrod import Player, random_choice
import random



class AverageCopier(Player):
    """The player will cooperate with probability p if the opponent's cooperation ratio is p."""

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
        """Randomly picks a strategy (not affected by history)."""
        if len(opponent.history) == 0:
            return random_choice(0.5)
        p = opponent.cooperations // len(opponent.history)
        rnd_num = random.random()
        if rnd_num < p:
            return 'C'
        return 'D'


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
        """Randomly picks a strategy (not affected by history)."""
        if len(opponent.history) == 0:
            return 'C'
        p = opponent.cooperations // len(opponent.history)
        return random_choice(p)
