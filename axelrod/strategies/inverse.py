from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice

C, D = Action.C, Action.D


class Inverse(Player):
    """A player who defects with a probability that diminishes relative to how
    long ago the opponent defected.

    Names:

    - Inverse: Original Name by Karol Langner
    """

    name = 'Inverse'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        """Looks at opponent history to see if they have defected.

        If so, player defection is inversely proportional to when this occurred.
        """

        # calculate how many turns ago the opponent defected
        index = next((index for index, value in
                      enumerate(opponent.history[::-1], start=1)
                      if value == D), None)

        if index is None:
            return C

        return random_choice(1 - 1 / abs(index))
