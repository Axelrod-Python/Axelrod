from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class Doubler(Player):
    """
    Cooperates except when the opponent has defected and
    the opponent's cooperation count is less than twice their defection count.

    Names:

    - Doubler: [Prison1998]_
    """

    name = 'Doubler'
    classifier = {
        'stochastic': False,
        'memory_depth': float('inf'),
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if not self.history:
            return C
        if (opponent.history[-1] == D and
                opponent.cooperations <= opponent.defections * 2):
            return D
        return C
