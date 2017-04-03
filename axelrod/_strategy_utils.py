"""Utilities used by various strategies"""
import itertools
from functools import lru_cache

from axelrod.player import update_history
from axelrod.actions import Actions
from axelrod.strategies.cooperator import Cooperator
from axelrod.strategies.defector import Defector


C, D = Actions.C, Actions.D


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
    offset: int, 0
        The amount of history to skip initially
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
    """Simulate one round vs opponent unless opponent has an inspection countermeasure."""
    if hasattr(opponent, 'foil_strategy_inspection'):
        return opponent.foil_strategy_inspection()
    else:
        return opponent.strategy(inspector)


def limited_simulate_play(player_1, player_2, h1):
    """Here we want to replay player_1's history to player_2, allowing
    player_2's strategy method to set any internal variables as needed. If you
    need a more complete simulation, see `simulate_play` in player.py. This
    function is specifically designed for the needs of MindReader."""
    h2 = inspect_strategy(player_1, player_2)
    update_history(player_1, h1)
    update_history(player_2, h2)


def simulate_match(player_1, player_2, strategy, rounds=10):
    """Simulates a number of matches."""
    for match in range(rounds):
        limited_simulate_play(player_1, player_2, strategy)


def calculate_scores(p1, p2, game):
    """Calculates the score for two players based their history"""
    s1, s2 = 0, 0
    for pair in zip(p1.history, p2.history):
        score = game.score(pair)
        s1 += score[0]
        s2 += score[1]
    return s1, s2


def look_ahead(player_1, player_2, game, rounds=10):
    """Looks ahead for `rounds` and selects the next strategy appropriately."""
    results = []
    # Simulate plays for `rounds` rounds
    players = {C: Cooperator(), D: Defector()}
    strategies = [C, D]
    for strategy in strategies:
        # Instead of a deepcopy, create a new opponent and play out the history
        opponent_ = player_2.clone()
        player_ = players[strategy]
        for h1 in player_1.history:
            limited_simulate_play(player_, opponent_, h1)

        simulate_match(player_, opponent_, strategy, rounds)
        results.append(calculate_scores(player_, opponent_, game))

    return strategies[results.index(max(results))]


@lru_cache()
def recursive_thue_morse(n):
    """The recursive definition of the Thue-Morse sequence. The first few terms
    of the Thue-Morse sequence are: 0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0 . . ."""

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
