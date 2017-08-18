import random
from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class OnceBitten(Player):
    """
    Cooperates once when the opponent defects, but if they defect twice in a row
    defaults to forgetful grudger for 10 turns defecting.

    Names:

    - Once Bitten: Original name by Holly Marissa
    """

    name = 'Once Bitten'
    classifier = {
        'memory_depth': 12,  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.mem_length = 10
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent: Player) -> Action:
        """
        Begins by playing C, then plays D for mem_length rounds if the opponent
        ever plays D twice in a row.
        """
        if self.grudge_memory >= self.mem_length:
            self.grudge_memory = 0
            self.grudged = False

        if len(opponent.history) < 2:
            return C

        if self.grudged:
            self.grudge_memory += 1
            return D
        elif not (C in opponent.history[-2:]):
            self.grudged = True
            return D
        return C



class FoolMeOnce(Player):
    """
    Forgives one D then retaliates forever on a second D.

    Names:

    - Fool me once: Original name by Marc Harper
    """

    name = 'Fool Me Once'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        if not opponent.history:
            return C
        if opponent.defections > 1:
            return D
        return C


class ForgetfulFoolMeOnce(Player):
    """
    Forgives one D then retaliates forever on a second D. Sometimes randomly
    forgets the defection count, and so keeps a secondary count separate from
    the standard count in Player.

    Names:

    - Forgetful Fool Me Once: Original name by Marc Harper
    """

    name = 'Forgetful Fool Me Once'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, forget_probability: float=0.05) -> None:
        """
        Parameters
        ----------
        forget_probability, float
            The probability of forgetting the count of opponent defections.
        """
        super().__init__()
        self.D_count = 0
        self._initial = C
        self.forget_probability = forget_probability

    def strategy(self, opponent: Player) -> Action:
        r = random.random()
        if not opponent.history:
            return self._initial
        if opponent.history[-1] == D:
            self.D_count += 1
        if r < self.forget_probability:
            self.D_count = 0
        if self.D_count > 1:
            return D
        return C

    def reset(self):
        super().reset()
        self.D_count = 0


class FoolMeForever(Player):
    """
    Fool me once, shame on me. Teach a man to fool me and I'll be fooled for
    the rest of my life.

    Names:

    - Fool Me Forever: Original name by Marc Harper
    """

    name = 'Fool Me Forever'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @staticmethod
    def strategy(opponent: Player) -> Action:
        if opponent.defections > 0:
            return C
        return D
