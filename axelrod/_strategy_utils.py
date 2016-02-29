"""Utilities used by various strategies"""
from axelrod import RoundRobin, update_history
from axelrod import Actions

from axelrod.strategies.cycler import Cycler

C, D = Actions.C, Actions.D

def detect_cycle(history, min_size=1, offset=0):
    """Detects cycles in the sequence history.

    Mainly used by hunter strategies.

    Parameters

    history: sequence of C and D
        The sequence to look for cycles within
    min_size: int, 1
        The minimum length of the cycle
    offset: int, 0
        The amount of history to skip initially
    """
    history_tail = history[-offset:]
    for i in range(min_size, len(history_tail) // 2):
        cycle = tuple(history_tail[:i])
        for j,  elem in enumerate(history_tail):
            if elem != cycle[j % len(cycle)]:
                break
        if j == len(history_tail) - 1:
            # We made it to the end, is the cycle itself a cycle?
            # I.E. CCC is not ok as cycle if min_size is really 2
            # Since this is the same as C
            return cycle
    return None


def limited_simulate_play(player_1, player_2, h1):
    """Here we want to replay player_1's history to player_2, allowing
    player_2's strategy method to set any internal variables as needed. If you
    need a more complete simulation, see `simulate_play` in player.py. This
    function is specifically designed for the needs of MindReader."""
    h2 = player_2.strategy(player_1)
    update_history(player_1, h1)
    update_history(player_2, h2)

def simulate_match(player_1, player_2, strategy, rounds=10):
    """Simulates a number of matches."""
    for match in range(rounds):
        limited_simulate_play(player_1, player_2, strategy)

def look_ahead(player_1, player_2, game, rounds=10):
    """Looks ahead for `rounds` and selects the next strategy appropriately."""
    results = []

    # Simulate plays for `rounds` rounds
    strategies = [C, D]
    for strategy in strategies:
        # Instead of a deepcopy, create a new opponent and play out the history
        opponent_ = player_2.clone()
        player_ = Cycler(strategy) # Either cooperator or defector
        for h1 in player_1.history:
            limited_simulate_play(player_, opponent_, h1)

        round_robin = RoundRobin(players=[player_, opponent_], game=game,
                                 turns=rounds)
        simulate_match(player_, opponent_, strategy, rounds)
        results.append(round_robin._calculate_scores(player_, opponent_)[0])

    return strategies[results.index(max(results))]
