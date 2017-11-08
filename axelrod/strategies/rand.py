from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice


class Random(Player):
    """A player who randomly chooses between cooperating and defecting.

    This strategy came 15th in Axelrod's original tournament.

    Names:

    - Random: [Axelrod1980]_
    - Lunatic: [Tzafestas2000]_
    """

    name = 'Random'
    classifier = {
        'memory_depth': 0,  # Memory-one Four-Vector = (p, p, p, p)
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, p: float=0.5) -> None:
        """
        Parameters
        ----------
        p, float
            The probability to cooperate

        Special Cases
        -------------
        Random(0) is equivalent to Defector
        Random(1) is equivalent to Cooperator
        """
        super().__init__()
        self.p = p
        if p in [0, 1]:
            self.classifier['stochastic'] = False

    def strategy(self, opponent: Player) -> Action:
        return random_choice(self.p)
