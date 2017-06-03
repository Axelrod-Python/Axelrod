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
