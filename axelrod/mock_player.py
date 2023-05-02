from itertools import cycle
from typing import List

from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class MockPlayer(Player):
    """Creates a mock player that plays a given sequence of actions. If
    no actions are given, or it runs out of actions,
    plays like Cooperator. Used for testing.

    Parameters
    ----------
    actions: List[Action], default []
        The sequence of actions played by the mock player.
    attributes: dict, default {}
        A dictionary of player attributes.
    """

    name = "Mock Player"
    attributes = {}

    def __init__(self, actions: List[Action] = None, attributes: dict = None) -> None:
        super().__init__()
        if not actions:
            actions = []
        if attributes:
            self.attributes = attributes
        self.actions = cycle(actions)

    def strategy(self, opponent: Player) -> Action:
        # Return the next saved action, if present.
        try:
            action = self.actions.__next__()
            return action
        except StopIteration:
            return C
