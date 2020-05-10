"""
Ultimatum Game.
"""

from enum import Enum
from typing import Optional, Tuple

import attr
from scipy import stats


class PlayerPosition(Enum):
    OFFERER = 1
    DECIDER = 2


@attr.s
class Outcome(object):
    position: "UltimatumPlayer" = attr.ib()
    offer: float = attr.ib()
    decision: bool = attr.ib()
    scores: Tuple[float, float] = attr.ib()


class UltimatumPlayer(object):
    """A generic abstract player of the ultimatum game."""

    name = "Ultimatum Player"

    # Possibly not always true, but set for now to prevent caching
    classifier = dict(stochastic=True)

    def __init__(self):
        self.history = []

    def reset(self) -> None:
        self.history = []

    def offer(self) -> float:
        """Returns a value between 0 and 1 for the proportion offered to the
        coplayer."""
        raise NotImplementedError

    def consider(self, offer: float) -> bool:
        """Decision rule for whether to accept the offer."""
        raise NotImplementedError

    def play(
        self, coplayer: "UltimatumPlayer", noise: Optional[float] = None
    ) -> Tuple[Outcome, Outcome]:
        """Play a game with this player as the offerer and the passed coplayer
        as the decider.  Appends Outcomes with offer decision and scores to the
        player's and coplayer's history, and returns."""
        offer = self.offer()
        decision = coplayer.consider(offer)
        # If the offer is accepted, return the split. Otherwise both players
        # receive nothing.
        if decision:
            scores = 1.0 - offer, offer
        else:
            scores = 0.0, 0.0
        outcome = Outcome(
            position=PlayerPosition.OFFERER,
            offer=offer,
            decision=decision,
            scores=scores,
        )
        coplayer_outcome = Outcome(
            position=PlayerPosition.DECIDER,
            offer=offer,
            decision=decision,
            scores=list(reversed(scores)),
        )
        self.history.append(outcome)
        coplayer.history.append(coplayer_outcome)
        return outcome, coplayer_outcome


class SimpleThresholdPlayer(UltimatumPlayer):
    """A simple Ultimatum game player with a fixed acceptance threshold and
    offer proportion."""

    name = "Simple Threshold Player"

    def __init__(
        self, offer_proportion: float = 0.5, lower_threshold: float = 0.5
    ):
        super().__init__()
        self.offer_proportion = offer_proportion
        self.lower_threshold = lower_threshold

    def __repr__(self) -> str:
        return "SimpleThresholdPlayer ({} | {})".format(
            self.offer_proportion, self.lower_threshold
        )

    def offer(self) -> float:
        return self.offer_proportion

    def consider(self, offer: float) -> bool:
        return offer >= self.lower_threshold


class AcceptanceThresholdPlayer(UltimatumPlayer):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion."""

    name = "Acceptance Threshold Player"

    def __init__(
        self,
        offer_proportion: float = 0.5,
        lower_threshold: float = 0.5,
        upper_threshold: float = 0.5,
    ):
        self.offer_proportion = offer_proportion
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def __repr__(self) -> str:
        return "AcceptanceThresholdPlayer ({} | [{}, {}])".format(
            self.offer_proportion, self.lower_threshold, self.upper_threshold
        )

    def offer(self) -> float:
        return self.offer_proportion

    def consider(self, offer: float) -> bool:
        return (offer >= self.lower_threshold) and (
            offer <= self.upper_threshold
        )


class DoubleThresholdsPlayer(UltimatumPlayer):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion."""

    name = "Double Thresholds Player"

    classifier = dict(stochastic=True)

    def __init__(
        self,
        lower_offer: float = 0.4,
        upper_offer: float = 0.6,
        lower_accept: float = 0.4,
        upper_accept: float = 0.6,
    ):
        self.lower_offer = lower_offer
        self.upper_offer = upper_offer
        self.lower_accept = lower_accept
        self.upper_accept = upper_accept
        self.offer_distribution = stats.uniform(
            loc=lower_offer, scale=upper_offer - lower_offer
        )
        self.init_kwargs = dict(
            lower_offer=lower_offer,
            upper_offer=upper_offer,
            lower_accept=lower_accept,
            upper_accept=upper_accept,
        )

    def __repr__(self) -> str:
        return "DoubleThresholdsPlayer ({}, {} | [{}, {}])".format(
            self.lower_offer,
            self.upper_offer,
            self.lower_accept,
            self.upper_accept,
        )

    def offer(self) -> float:
        # print(self.lower_offer, self.upper_offer)
        return self.offer_distribution.rvs()

    def consider(self, offer: float) -> bool:
        return (offer >= self.lower_accept) and (offer <= self.upper_accept)


class DistributionPlayer(UltimatumPlayer):
    """A stochastic player of the ultimatum game."""

    name = "Distribution Player"

    def __init__(
        self,
        offer_distribution: Optional[stats.distributions.rv_continuous] = None,
        acceptance_distribution: Optional[
            stats.distributions.rv_continuous
        ] = None,
    ):
        if not offer_distribution:
            offer_distribution = stats.norm(0.5, 0.1)  # pragma: no cover
        if not acceptance_distribution:
            acceptance_distribution = stats.norm(0.5, 0.1)  # pragma: no cover
        self.offer_distribution = offer_distribution
        self.acceptance_distribution = acceptance_distribution

    def __repr__(self) -> str:
        return "DistributionThresholdPlayer"

    def offer(self) -> float:
        return self.offer_distribution.rvs()

    def consider(self, offer: float) -> bool:
        return self.acceptance_distribution.rvs() <= offer
