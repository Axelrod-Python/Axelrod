"""Utilities used by various strategies."""

import itertools
from functools import lru_cache

from axelrod.action import Action
from axelrod.player import update_history
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
    oponnent: Player
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


def _limited_simulate_play(player_1, player_2, h1):
    """Simulates a player's move.

    After inspecting player_2's next move (allowing player_2's strategy
    method to set any internal variables as needed), update histories
    for both players. Note that player_1's move is an argument.

    If you need a more complete simulation, see `simulate_play` in
    player.py. This function is specifically designed for the needs
    of MindReader.

    Parameters
    ----------
    player_1: Player
        The player whose move is already known.
    player_2: Player
        The player the we want to inspect.
    h1: Action
        The next action for first player.
    """
    h2 = inspect_strategy(player_1, player_2)
    update_history(player_1, h1)
    update_history(player_2, h2)


def simulate_match(player_1, player_2, strategy, rounds=10):
    """Simulates a number of rounds with a constant strategy.

    Parameters
    ----------
    player_1: Player
        The player that will have a constant strategy.
    player_2: Player
        The player we want to simulate.
    strategy: Action
        The constant strategy to use for first player.
    rounds: int
        The number of rounds to play.
    """
    for match in range(rounds):
        _limited_simulate_play(player_1, player_2, strategy)


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


def look_ahead(player_1, player_2, game, rounds=10):
    """Returns a constant action that maximizes score by looking ahead.

    Parameters
    ----------
    player_1: Player
        The player that will look ahead.
    player_2: Player
        The opponent that will be inspected.
    game: Game
        The Game object used to score rounds.
    rounds: int
        The number of rounds to look ahead.

    Returns
    -------
    Action
        The action that maximized score if it is played constantly.
    """
    results = {}
    possible_strategies = {C: Cooperator(), D: Defector()}
    for action, player in possible_strategies.items():
        # Instead of a deepcopy, create a new opponent and replay the history to it.
        opponent_ = player_2.clone()
        for h in player_1.history:
            _limited_simulate_play(player, opponent_, h)

        # Now play forward with the constant strategy.
        simulate_match(player, opponent_, action, rounds)
        results[action] = _calculate_scores(player, opponent_, game)

    return C if results[C] > results[D] else D


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
