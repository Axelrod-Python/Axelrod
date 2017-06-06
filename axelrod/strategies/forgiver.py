from axelrod.actions import Action, Actions
from axelrod.player import Player

C, D = Actions.C, Actions.D


class Forgiver(Player):
    """
    A player starts by cooperating however will defect if at any point
    the opponent has defected more than 10 percent of the time

    Names:

    - Forgiver: Original name by Thomas Campbell
    """

    name = 'Forgiver'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        """
        Begins by playing C, then plays D if the opponent has defected more
        than 10 percent of the time.
        """
        if opponent.defections > len(opponent.history) / 10.0:
            return D
        return C


class ForgivingTitForTat(Player):
    """
    A player starts by cooperating however will defect if at any point, the
    opponent has defected more than 10 percent of the time, and their most
    recent decision was defect.

    Names:

    - Forgiving Tit For Tat: Original name by Thomas Campbell
    """

    name = 'Forgiving Tit For Tat'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        """
        Begins by playing C, then plays D if the opponent has defected more than
        10 percent of the time and their most recent decision was defect.
        """
        if opponent.defections > len(opponent.history) / 10:
            return opponent.history[-1]
        return C
