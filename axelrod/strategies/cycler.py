
from axelrod import Player


class AntiCycler(Player):
    """
    A player that follows a sequence of plays that contains no cycles:
    C CD CCD CCCD CCCCD CCCCCD ...
    """

    name = 'AntiCycler'
    behaviour = {
        'memory_depth': float('inf')
    }

    def __init__(self):
        Player.__init__(self)
        self.cycle_length = 1
        self.cycle_counter = 0

    def strategy(self, opponent):
        if self.cycle_counter < self.cycle_length:
            self.cycle_counter += 1
            return 'C'
        else:
            self.cycle_length += 1
            self.cycle_counter = 0
            return 'D'

    def reset(self):
        Player.reset(self)
        self.cycle_length = 1
        self.cycle_counter = 0


class Cycler(Player):
    """A player that repeats a given sequence indefinitely."""

    name = 'Cycler'
    behaviour = {
        'memory_depth': 1
    }

    def __init__(self, cycle="CCD"):
        Player.__init__(self)
        self.cycle = cycle
        self.name += " " + cycle
        self.memory_depth = len(cycle)

    def strategy(self, opponent):
        curent_round = len(self.history)
        index = curent_round % len(self.cycle)
        return self.cycle[index]


class CyclerCCD(Cycler):
    def __init__(self, cycle="CCD"):
        Cycler.__init__(self, cycle=cycle)


class CyclerCCCD(Cycler):
    def __init__(self, cycle="CCCD"):
        Cycler.__init__(self, cycle=cycle)


class CyclerCCCCCD(Cycler):
    def __init__(self, cycle="CCCCCD"):
        Cycler.__init__(self, cycle=cycle)
