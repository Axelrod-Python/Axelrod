from collections import defaultdict
from itertools import cycle
import warnings

from axelrod.actions import Actions, Action
from axelrod.player import Player, update_history, update_state_distribution

from typing import List, Tuple

C, D = Actions.C, Actions.D


class MockPlayer(Player):
    """Creates a mock player that plays a given sequence of actions. If
    no actions are given, plays like Cooperator. Used for testing.
    """

    name = "Mock Player"

    def __init__(self, actions: List[Action] = None) -> None:
        super().__init__()
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
