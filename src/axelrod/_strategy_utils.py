"""Utilities used by various strategies."""

import itertools
from functools import lru_cache

from axelrod.action import Action
from axelrod.strategies.cooperator import Cooperator
from axelrod.strategies.defector import Defector

C, D = Action.C, Action.D


def detect_cycle(history, min_size=1, max_size=12, offset=0):
    """Detects cycles in the sequence history.

    Mainly used by hunter strategies.

    Parameters
    ----------
    history: sequence of C and D
        The sequence to look for cycles within
    min_size: int, 1
        The minimum length of the cycle
    max_size: int, 12
        The maximum length of the cycle
    offset: int, 0
        The amount of history to skip initially

    Returns
    -------
    Tuple of C and D
        The cycle detected in the input history
    """
    history_tail = history[offset:]
    new_max_size = min(len(history_tail) // 2, max_size)
    for i in range(min_size, new_max_size + 1):
        has_cycle = True
        cycle = tuple(history_tail[:i])
        for j, elem in enumerate(history_tail):
            if elem != cycle[j % len(cycle)]:
                has_cycle = False
                break
        if has_cycle:
            return cycle
    return None


@lru_cache()
def recursive_thue_morse(n):
    """The recursive definition of the Thue-Morse sequence.

    The first few terms of the Thue-Morse sequence are:
        0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0 . . .
    """

    if n == 0:
        return 0
    if n % 2 == 0:
        return recursive_thue_morse(n / 2)
    if n % 2 == 1:
        return 1 - recursive_thue_morse((n - 1) / 2)


def thue_morse_generator(start=0):
    """A generator for the Thue-Morse sequence."""
    for n in itertools.count(start):
        yield recursive_thue_morse(n)
