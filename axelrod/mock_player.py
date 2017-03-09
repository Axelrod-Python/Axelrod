import warnings
from axelrod.actions import Actions, Action
from axelrod.player import Player, update_history, update_state_distribution
from collections import defaultdict
from itertools import cycle

from typing import List, Tuple

C, D = Actions.C, Actions.D


class MockPlayer(Player):
    """Creates a mock player that copies a history and state distribution to
    simulate a history of play, and then plays a given sequence of actions. If
    no actions are given, plays like Cooperator.
    """

    name = "Mock Player"

    def __init__(self, actions: List[Action] =None, history: List[Action] =None, state_dist: defaultdict =None) -> None:
        # Need to retain history for opponents that examine opponents history
        # Do a deep copy just to be safe
        super().__init__()
        if history:
            # Make sure we both copy the history and get the right counts
            # for cooperations and defections.
            for action in history:
                update_history(self, action)
        if state_dist:
            self.state_distribution = dict(state_dist)
        if actions:
            self.actions = cycle(actions)
        else:
            self.actions = iter([])

    def strategy(self, opponent: Player) -> Action:
        # Return the next saved action, if present.
        try:
            action = self.actions.__next__()
            return action
        except StopIteration:
            return C


def simulate_play(player1: Player, player2: Player, action1: Action =None, action2: Action =None) -> Tuple[Action, Action]:
    """
    Simulates play with or without forced history. If action1 and action2 are given, these
    actions are enforced in the players strategy. This generally should not be
    necessary, but various tests may force impossible or unlikely histories.
    """

    if action1 and action2:
        mock_player1 = MockPlayer(actions=[action1], history=player1.history)
        mock_player2 = MockPlayer(actions=[action2], history=player2.history)
        # Force plays
        s1 = player1.strategy(mock_player2)
        s2 = player2.strategy(mock_player1)
        if (s1 != action1) or (s2 != action2):
            warnings.warn(
            "Simulated play mismatch with expected history: Round was "
            "({}, {}) but ({}, {}) was expected for player: {}".format(
                s1, s2, action1, action2, str(player1))
            )
        # Record intended history
        # Update Cooperation / Defection counts
        update_history(player1, action1)
        update_history(player2, action2)
        update_state_distribution(player1, action1, action2)
        update_state_distribution(player2, action2, action1)
        return (s1, s2)
    else:
        s1 = player1.strategy(player2)
        s2 = player2.strategy(player1)
        # Record history
        update_history(player1, s1)
        update_history(player2, s2)
        update_state_distribution(player1, s1, s2)
        update_state_distribution(player2, s2, s1)
        return (s1, s2)
