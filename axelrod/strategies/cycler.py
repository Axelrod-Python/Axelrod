from axelrod import Actions, Player, init_args

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

    def __init__(self):
        Player.__init__(self)
        self.cycle_length = 1
        self.cycle_counter = 0

    def strategy(self, opponent):
        if self.cycle_counter < self.cycle_length:
            self.cycle_counter += 1
            return Actions.C
        else:
            self.cycle_length += 1
            self.cycle_counter = 0
            return Actions.D

    def reset(self):
        Player.reset(self)
        self.cycle_length = 1
        self.cycle_counter = 0


class Cycler(Player):
    """A player that repeats a given sequence indefinitely."""

    name = 'Cycler'
    classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @init_args
    def __init__(self, cycle="CCD"):
        """This strategy will repeat the parameter `cycle` endlessly,
        e.g. C C D C C D C C D ...

        Special Cases
        -------------
        Cooperator is equivalent to Cycler("C")
        Defector   is equivalent to Cycler("D")
        Alternator is equivalent to Cycler("CD")

        """
        Player.__init__(self)
        self.cycle = cycle
        self.name = "Cycler {}".format(cycle)
        self.classifier['memory_depth'] = len(cycle) - 1

    def strategy(self, opponent):
        curent_round = len(self.history)
        index = curent_round % len(self.cycle)
        return self.cycle[index]


class CyclerDC(Cycler):

    name = 'Cycler DC'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 1

    @init_args
    def __init__(self, cycle="DC"):
        Cycler.__init__(self, cycle=cycle)


class CyclerCCD(Cycler):

    name = 'Cycler CCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 2

    @init_args
    def __init__(self, cycle="CCD"):
        Cycler.__init__(self, cycle=cycle)


class CyclerDDC(Cycler):

    name = 'Cycler DDC'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 2

    @init_args
    def __init__(self, cycle="DDC"):
        Cycler.__init__(self, cycle=cycle)


class CyclerCCCD(Cycler):

    name = 'Cycler CCCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 3

    @init_args
    def __init__(self, cycle="CCCD"):
        Cycler.__init__(self, cycle=cycle)


class CyclerCCCCCD(Cycler):

    name = 'Cycler CCCCCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 5

    @init_args
    def __init__(self, cycle="CCCCCD"):
        Cycler.__init__(self, cycle=cycle)


class CyclerCCCDCD(Cycler):

    name = 'Cycler CCCDCD'
    classifier = copy.copy(Cycler.classifier)
    classifier['memory_depth'] = 5

    @init_args
    def __init__(self, cycle="CCCDCD"):
        Cycler.__init__(self, cycle=cycle)
