"""Holds UltimatumPosition"""

from axelrod.prototypes import Position


# TODO(5.0): Move to someplace better.
class UltimatumPosition(Position):
    OFFERER = 1
    DECIDER = 2
