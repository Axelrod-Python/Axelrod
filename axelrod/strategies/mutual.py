from axelrod.action import Action
from axelrod.player import Player
from axelrod.random_ import random_choice

C, D = Action.C, Action.D


class Desperate(Player):
    """A player that only cooperates after mutual defection.

    Names:

    - Desperate: [Berg2015]_"""

    name = "Desperate"
    classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return random_choice()
        if self.history[-1] == D and opponent.history[-1] == D:
            return C
        return D


class Hopeless(Player):
    """A player that only defects after mutual cooperation.

    Names:

    - Hopeless: [Berg2015]_"""

    name = "Hopeless"
    classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return random_choice()
        if self.history[-1] == C and opponent.history[-1] == C:
            return D
        return C


class Willing(Player):
    """A player that only defects after mutual defection.

    Names:

    - Willing: [Berg2015]_"""

    name = "Willing"
    classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if not opponent.history:
            return random_choice()
        if self.history[-1] == D and opponent.history[-1] == D:
            return D
        return C
