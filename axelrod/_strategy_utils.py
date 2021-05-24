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


def inspect_strategy(inspector, opponent):
    """Inspects the strategy of an opponent.

    Simulate one round of play with an opponent, unless the opponent has
    an inspection countermeasure.

    Parameters
    ----------
    inspector: Player
        The player doing the inspecting
    opponent: Player
        The player being inspected

    Returns
    -------
    Action
        The action that would be taken by the opponent.
    """
    if hasattr(opponent, "foil_strategy_inspection"):
        return opponent.foil_strategy_inspection()
    else:
        return opponent.strategy(inspector)


def _calculate_scores(p1, p2, game):
    """Calculates the scores for two players based their history.

    Parameters
    ----------
    p1: Player
        The first player.
    p2: Player
        The second player.
    game: Game
        Game object used to score rounds in the players' histories.

    Returns
    -------
    int, int
        The scores for the two input players.
    """
    s1, s2 = 0, 0
    for pair in zip(p1.history, p2.history):
        score = game.score(pair)
        s1 += score[0]
        s2 += score[1]
    return s1, s2


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
