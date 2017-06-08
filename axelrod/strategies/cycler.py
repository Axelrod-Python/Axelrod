import copy
import itertools

from axelrod.actions import Actions, Action, str_to_actions
from axelrod.player import Player

C, D = Actions.C, Actions.D


class AntiCycler(Player):
    """
    A player that follows a sequence of plays that contains no cycles:
    CDD  CD  CCD CCCD CCCCD ...

    Names:

    - Anti Cycler: Original name by Marc Harper
    """

    name = 'AntiCycler'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self) -> None:
        super().__init__()
        self.cycle_length = 1
        self.cycle_counter = 0
        self.first_three = self._get_first_three()

    @staticmethod
    def _get_first_three():
        return [C, D, D]

    def strategy(self, opponent: Player) -> Action:
        while self.first_three:
            return self.first_three.pop(0)
        if self.cycle_counter < self.cycle_length:
            self.cycle_counter += 1
            return C
        else:
            self.cycle_length += 1
            self.cycle_counter = 0
            return D

    def reset(self):
        super().reset()
        self.cycle_length = 1
        self.cycle_counter = 0
        self.first_three = self._get_first_three()


class Cycler(Player):
    """
    A player that repeats a given sequence indefinitely.

    Names:

    - Cycler: Original name by Marc Harper
    """

    name = 'Cycler'
    classifier = {
        'memory_depth': 2,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, cycle: str = "CCD") -> None:
        """This strategy will repeat the parameter `cycle` endlessly,
        e.g. C C D C C D C C D ...

        Special Cases
        -------------
        Cooperator is equivalent to Cycler("C")
        Defector   is equivalent to Cycler("D")
        Alternator is equivalent to Cycler("CD")

        """
        super().__init__()
        self.cycle_str = cycle
        self.cycle = self.get_new_itertools_cycle()
        self.classifier['memory_depth'] = len(cycle) - 1

    def get_new_itertools_cycle(self):
        return itertools.cycle(str_to_actions(self.cycle_str))

    def strategy(self, opponent: Player) -> Action:
        return next(self.cycle)

    def reset(self):
        super(Cycler, self).reset()
        self.cycle = self.get_new_itertools_cycle()


class CyclerDC(Cycler):
    """
    Cycles D, C

    Names:

    - Cycler DC: Original name by Marc Harper
    """
    name = 'Cycler DC'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 1

    def __init__(self) -> None:
        super().__init__(cycle="DC")


class CyclerCCD(Cycler):
    """
    Cycles C, C, D

    Names:

    - Cycler CCD: Original name by Marc Harper
    - Periodic player CCD: [Mittal2009]_
    """
    name = 'Cycler CCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 2

    def __init__(self) -> None:
        super().__init__(cycle="CCD")


class CyclerDDC(Cycler):
    """
    Cycles D, D, C

    Names:

    - Cycler DDC: Original name by Marc Harper
    - Periodic player DDC: [Mittal2009]_
    """
    name = 'Cycler DDC'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 2

    def __init__(self) -> None:
        super().__init__(cycle="DDC")


class CyclerCCCD(Cycler):
    """
    Cycles C, C, C, D

    Names:

    - Cycler CCCD: Original name by Marc Harper
    """
    name = 'Cycler CCCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 3

    def __init__(self) -> None:
        super().__init__(cycle="CCCD")


class CyclerCCCCCD(Cycler):
    """
    Cycles C, C, C, C, C, D

    Names:

    - Cycler CCCD: Original name by Marc Harper
    """
    name = 'Cycler CCCCCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 5

    def __init__(self) -> None:
        super().__init__(cycle="CCCCCD")


class CyclerCCCDCD(Cycler):
    """
    Cycles C, C, C, D, C, D

    Names:

    - Cycler CCCDCD: Original name by Marc Harper
    """

    name = 'Cycler CCCDCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 5

    def __init__(self) -> None:
        super().__init__(cycle="CCCDCD")
