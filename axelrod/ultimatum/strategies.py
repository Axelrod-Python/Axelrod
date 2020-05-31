"""Implements strategies for ultimatum."""

from typing import Optional

from scipy import stats

from .player import UltimatumPlayer
from .position import UltimatumPosition


class ConsiderThresholdPlayer(object):
    """Creates the consider function of an ultimatum player that only accepts
    offer in the provided thresholds."""

    lower_threshold, upper_threshold = None, None

    def set_thresholds(self, lower: float, upper: float = 1.0) -> None:
        self.lower_threshold, self.upper_threshold = lower, upper

    def consider(self, offer: float) -> bool:
        assert self.lower_threshold is not None
        return self.lower_threshold <= offer <= self.upper_threshold


class ConstantOfferPlayer(object):
    """Creates the consider function of an ultimatum player that only accepts
    offer in the provided thresholds."""

    offer_proportion = None

    def set_offer_proportion(self, offer_proportion: float) -> None:
        self.offer_proportion = offer_proportion

    def offer(self) -> float:
        assert self.offer_proportion is not None
        return self.offer_proportion


class SimpleThresholdPlayer(
    ConsiderThresholdPlayer, ConstantOfferPlayer, UltimatumPlayer
):
    """A simple Ultimatum game player with a fixed acceptance threshold and
    offer proportion.

    Source: Axelrod library
    """

    name = "Simple Threshold Player"
    classifier = dict(stochastic=False)

    def __init__(
        self, offer_proportion: float = 0.5, lower_threshold: float = 0.5
    ):
        super().__init__()
        self.set_thresholds(lower_threshold)
        self.set_offer_proportion(offer_proportion)

    def __repr__(self) -> str:
        return "SimpleThresholdPlayer ({} | {})".format(
            self.offer_proportion, self.lower_threshold
        )


class AcceptanceThresholdPlayer(
    ConsiderThresholdPlayer, ConstantOfferPlayer, UltimatumPlayer
):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion.

    Source: Axelrod library
    """

    name = "Acceptance Threshold Player"
    classifier = dict(stochastic=False)

    def __init__(
        self,
        offer_proportion: float = 0.5,
        lower_threshold: float = 0.5,
        upper_threshold: float = 0.5,
    ):
        super().__init__()
        self.set_offer_proportion(offer_proportion)
        self.set_thresholds(lower_threshold, upper_threshold)

    def __repr__(self) -> str:
        return "AcceptanceThresholdPlayer ({} | [{}, {}])".format(
            self.offer_proportion, self.lower_threshold, self.upper_threshold
        )


class DoubleThresholdsPlayer(ConsiderThresholdPlayer, UltimatumPlayer):
    """A simple Ultimatum game player with fixed acceptance thresholds (upper
    and lower) and a fixed offer proportion.

    Source: Axelrod library
    """

    name = "Double Thresholds Player"
    classifier = dict(stochastic=False)

    def __init__(
        self,
        lower_offer: float = 0.4,
        upper_offer: float = 0.6,
        lower_accept: float = 0.4,
        upper_accept: float = 0.6,
    ):
        super().__init__()
        self.lower_offer = lower_offer
        self.upper_offer = upper_offer
        self.set_thresholds(lower_accept, upper_accept)
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
            self.init_kwargs["lower_accept"],
            self.init_kwargs["upper_accept"],
        )

    def offer(self) -> float:
        # print(self.lower_offer, self.upper_offer)
        return self.offer_distribution.rvs()


class DistributionPlayer(UltimatumPlayer):
    """A stochastic player of the ultimatum game.

    Source: Axelrod library
    """

    name = "Distribution Player"
    classifier = dict(stochastic=True)

    def __init__(
        self,
        offer_distribution: Optional[stats.distributions.rv_continuous] = None,
        acceptance_distribution: Optional[
            stats.distributions.rv_continuous
        ] = None,
    ):
        super().__init__()
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


class BinarySearchOfferPlayer(ConsiderThresholdPlayer, UltimatumPlayer):
    """Adjusts offers in a binary search fashion to try to find a lowest-
    acceptable offer.  Considers offers similar to DoubleThresholdsPlayer.

    Source: Axelrod library
    """

    name = "Binary Search Offers Player"
    classifier = dict(stochastic=False)

    def __init__(
        self, lower_threshold: float = 0.5, upper_threshold: float = 1.0,
    ):
        super().__init__()
        self.set_thresholds(lower_threshold, upper_threshold)
        self.offer_size = 0.5
        self.step_size = 0.25

    def __repr__(self) -> str:
        return "BinarySearchOfferPlayer [{}, {}]".format(
            self.lower_threshold, self.upper_threshold
        )

    def offer(self) -> float:
        if self.history.offers:
            # If prior offer was accepted offer less; otherwise more
            delta = self.step_size * (
                -1
                if self.history.offers[-1].actions[UltimatumPosition.DECIDER]
                else 1
            )
            self.offer_size += delta
            self.step_size *= 0.5

        return self.offer_size


class TitForTatOfferPlayer(ConsiderThresholdPlayer, UltimatumPlayer):
    """Extend to an opponent the last offer they extended to this player.
    Considers offers similar to DoubleThresholdsPlayer.

    Source: Axelrod library
    """

    name = "TitForTat Offer Player"
    classifier = dict(stochastic=False)

    def __init__(
        self,
        default_offer: float = 0.5,
        lower_threshold: float = 0.5,
        upper_threshold: float = 1.0,
    ):
        super().__init__()
        self.default_offer = default_offer
        self.set_thresholds(lower_threshold, upper_threshold)

    def __repr__(self) -> str:
        return "TitForTatOfferPlayer ({} | [{}, {}])".format(
            self.default_offer, self.lower_threshold, self.upper_threshold
        )

    def offer(self) -> float:
        if self.history.decisions:
            return self.history.decisions[-1].actions[UltimatumPosition.OFFERER]
        return self.default_offer


class TitForTatDecisionPlayer(ConstantOfferPlayer, UltimatumPlayer):
    """Accept an offer from an opponent only if the opponent accepted your last
    offer.  Makes offers at a constant level, similar to similar to
    SimpleThresholdPlayer.

    Source: Axelrod library
    """

    name = "TitForTat Decision Player"
    classifier = dict(stochastic=False)

    def __init__(
        self, offer_proportion: float = 0.5, default_acceptance: bool = True
    ):
        super().__init__()
        self.set_offer_proportion(offer_proportion)
        self.default_acceptance = default_acceptance

    def __repr__(self) -> str:
        return "TitForTatDecisionPlayer ({}, {})".format(
            self.offer_proportion, self.default_acceptance
        )

    def consider(self, offer: float) -> bool:
        if self.history.offers:
            return self.history.offers[-1].actions[UltimatumPosition.DECIDER]
        return self.default_acceptance


class RejectionLiftPlayer(ConstantOfferPlayer, UltimatumPlayer):
    """Rejects first two offers.  After assumes that last increase in response
    to a rejection will be the next increase in response to rejection.  Then
    calculates cost-benefit of another rejection, discounting future play.
    Makes offers at a constant level, similar to similar to
    SimpleThresholdPlayer.

    Source: Axelrod library
    """

    name = "Rejection-Lift Player"
    classifier = dict(stochastic=False)

    def __init__(self, offer_proportion: float = 0.5, discount: float = 0.9):
        super().__init__()
        self.set_offer_proportion(offer_proportion)
        self.discount = discount
        self.future_weight = self.discount / (1.0 - self.discount)

    def __repr__(self) -> str:
        return "RejectionLiftPlayer ({}, {})".format(
            self.offer_proportion, self.discount
        )

    def _get_lift(self) -> float:
        response = None
        for h in reversed(self.history.decisions):
            if response is not None:
                if not h.actions[UltimatumPosition.DECIDER]:
                    return response - h.actions[UltimatumPosition.OFFERER]
            response = h.actions[UltimatumPosition.OFFERER]

    def consider(self, offer: float) -> bool:
        if len(self.history.decisions) < 2:
            return False

        # Cost/benefit of rejecting here.
        cost = offer
        benefit = self._get_lift() * self.future_weight

        return benefit < cost
