from itertools import cycle
from typing import List

from axelrod.action import Action
from axelrod.player import IpdPlayer

C, D = Action.C, Action.D


class MockPlayer(IpdPlayer):
    """Creates a mock player that plays a given sequence of actions. If
    no actions are given, plays like Cooperator. Used for testing.
    """

    name = "Mock IpdPlayer"

    def __init__(self, actions: List[Action] = None) -> None:
        super().__init__()
        if not actions:
            actions = []
        self.actions = cycle(actions)

    def strategy(self, opponent: IpdPlayer) -> Action:
        # Return the next saved action, if present.
        try:
            action = self.actions.__next__()
            return action
        except StopIteration:
            return C
