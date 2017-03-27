from axelrod.actions import Actions, Action, str_to_actions
from axelrod.player import Player
import itertools
import copy


class AntiCycler(Player):
    """
    A player that follows a sequence of plays that contains no cycles:
    C CD CCD CCCD CCCCD CCCCCD ...
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

    def strategy(self, opponent: Player) -> Action:
        if self.cycle_counter < self.cycle_length:
            self.cycle_counter += 1
            return Actions.C
        else:
            self.cycle_length += 1
            self.cycle_counter = 0
            return Actions.D

    def reset(self):
        super().reset()
        self.cycle_length = 1
        self.cycle_counter = 0


class Cycler(Player):
    """A player that repeats a given sequence indefinitely."""

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
        self.name = "Cycler {}".format(cycle)
        self.classifier['memory_depth'] = len(cycle) - 1

    def get_new_itertools_cycle(self):
        return itertools.cycle(str_to_actions(self.cycle_str))

    def strategy(self, opponent: Player) -> Action:
        return next(self.cycle)

    def reset(self):
        super(Cycler, self).reset()
        self.cycle = self.get_new_itertools_cycle()


class CyclerDC(Cycler):

    name = 'Cycler DC'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 1

    def __init__(self, cycle="DC") -> None:
        super().__init__(cycle=cycle)


class CyclerCCD(Cycler):

    name = 'Cycler CCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 2

    def __init__(self, cycle="CCD") -> None:
        super().__init__(cycle=cycle)


class CyclerDDC(Cycler):

    name = 'Cycler DDC'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 2

    def __init__(self, cycle="DDC") -> None:
        super().__init__(cycle=cycle)


class CyclerCCCD(Cycler):

    name = 'Cycler CCCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 3

    def __init__(self, cycle="CCCD") -> None:
        super().__init__(cycle=cycle)


class CyclerCCCCCD(Cycler):

    name = 'Cycler CCCCCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 5

    def __init__(self, cycle="CCCCCD") -> None:
        super().__init__(cycle=cycle)


class CyclerCCCDCD(Cycler):

    name = 'Cycler CCCDCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 5

    def __init__(self, cycle="CCCDCD") -> None:
        super().__init__(cycle=cycle)
