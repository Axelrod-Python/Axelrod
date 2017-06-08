from axelrod.actions import Actions, Action
from axelrod.player import Player

C, D = Actions.C, Actions.D


class Resurrection(Player):
    """
    A player starts by cooperating and defects if the number of rounds
    played by the player is greater than five and the last five rounds
    are defections.

    Otherwise, the strategy plays like Tit-for-tat.

    Names:
    - Resurrection: [Eckhart2015]_
    """

    # These are various properties for the strategy
    name = 'Resurrection'
    classifier = {
        'memory_depth': 5,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            return C
        if len(self.history) >= 5 and self.history[-5:] == [D, D, D, D, D]:
            return D
        else:
            return opponent.history[-1]


class DoubleResurrection(Player):
    """
    A player starts by cooperating and defects if the number of rounds
    played by the player is greater than five and the last five rounds
    are cooperations.

    If the last five rounds were defections, the player cooperates.

    Names:
    - DoubleResurrection: [Eckhart2015]_
    """

    name = 'DoubleResurrection'
    classifier = {
        'memory_depth': 5,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def strategy(self, opponent: Player) -> Action:
        if len(self.history) == 0:
            return C
        if len(self.history) >= 5 and self.history[-5:] == [C, C, C, C, C]:
            return D
        elif len(self.history) >= 5 and self.history[-5:] == [D, D, D, D, D]:
            return C
        else:
            return opponent.history[-1]
