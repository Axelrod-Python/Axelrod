"""Define player for Ultimatum game

The Ultimatum game involves two players.  The first player chooses how to split
1.0 point, offering some portion to the other player.  The second player decides
if they accept or reject the offer.  If the offer is accepted, then the second
player gets the offered amount, and the first player gets the remainder of the
1.0 point.  If the offer is rejected, then neither player gets any points.

The game has two roles or Positions, an Offerer and a Decider.  Every
UltimatumPlayer needs to have a strategy for how to offer and how to decide.

This file also defines a history class which contains functionality for looking
up only offer history and only decision history.
"""

from axelrod.prototypes import BasePlayer
from .game_params import ultimatum_static_params
from .history import UltimatumHistory


class UltimatumPlayer(BasePlayer):
    """A generic abstract player of the ultimatum game."""

    name = "Ultimatum Player"
    classifier = dict(stochastic=False)

    def history_factory(self):
        return UltimatumHistory()

    def __init__(self):
        # TODO(5.0): Between the two ultimatum game_params, the only difference
        #  is after the first round is generated.  Maybe we want to separate
        #  this from the rest of the game_params, in order to have a canonical
        #  game_params for the game type.
        self.game_params = ultimatum_static_params
        super().__init__()

    def offer(self) -> float:
        """Returns a value between 0 and 1 for the proportion offered to the
        coplayer."""
        raise NotImplementedError

    def consider(self, offer: float) -> bool:
        """Decision rule for whether to accept the offer.  True means accept,
        and false means reject."""
        raise NotImplementedError

    def set_match_attributes(self, **match_attributes):
        pass
