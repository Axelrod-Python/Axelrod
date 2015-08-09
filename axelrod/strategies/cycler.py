import functools
import itertools

from axelrod import Player


class AntiCycler(Player):
    """
    A player that follows a sequence of plays that contains no cycles:
    C CD CCD CCCD CCCCD CCCCCD ...
    """

    name = 'AntiCycler'
    memory_depth = float('inf')

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
    memory_depth = 1

    def __init__(self, cycle="CCD"):
        Player.__init__(self)
        self.cycle = cycle
        self.cycle_iter = itertools.cycle(self.cycle)
        self.name += " " + cycle
        self.memory_depth = len(cycle)

    def strategy(self, opponent):
        return self.cycle_iter.next()
        #curent_round = len(history) + 1
        #index = curent_round % len(self.cycle)
        #return self.cycle[index]

    def reset(self):
        Player.reset(self)
        self.cycle_iter = itertools.cycle(self.cycle)


CyclerCCD = functools.partial(Cycler, "CCD")
CyclerCCCD = functools.partial(Cycler, "CCCD")
CyclerCCCCCD = functools.partial(Cycler, "CCCCCD")
