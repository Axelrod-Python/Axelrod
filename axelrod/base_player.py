import inspect
from typing import Optional, Tuple

import axelrod as axl


class BasePlayer(object):

    def __init__(self):
        pass

    def strategy(self, opponent: "BasePlayer") -> axl.Action:
        """Calculates the action of this player against the provided
        opponent."""
        raise NotImplementedError()

    def play(
        self,
        opponent: "BasePlayer",
        noise: float = 0,
        strategy_holder: Optional["BasePlayer"] = None,
    ) -> Tuple[axl.Action, axl.Action]:
        """This pits two players against each other, using the passed strategy
        holder, if provided."""
        raise NotImplementedError()

    def clone(self) -> "BasePlayer":
        """Clones the player without history, reapplying configuration
        parameters as necessary."""
        raise NotImplementedError()

    def reset(self):
        """Resets a player to its initial state

        This method is called at the beginning of each match (between a pair
        of players) to reset a player's state to its initial starting point.
        It ensures that no 'memory' of previous matches is carried forward.
        """
        raise NotImplementedError()
