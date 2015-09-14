from axelrod import Player
import random


class Inverse(Player):
    """A player who defects with a probability that diminishes relative to how
    long ago the opponent defected."""

    name = 'Inverse'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent):
        """Looks at opponent history to see if they have defected.

        If so, player defection is inversely proportional to when this occurred.
        """

        index = next((index for index, value in enumerate(opponent.history, start=1) if value == 'D'), None)

        if index is None:
            return 'C'

        rnd_num = random.random()

        if rnd_num < 1 / float(abs(index)):
            return 'D'
        return 'C'
