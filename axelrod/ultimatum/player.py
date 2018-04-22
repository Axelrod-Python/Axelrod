"""
Ultimatum Game .
"""

from scipy import stats


def play(player, coplayer):
    offer = player.offer()
    decision = coplayer.consider(offer)
    # If the offer is accepted, return the split. Otherwise both players
    # receive nothing.
    if decision:
        return 1. - offer, offer
    return 0., 0.


class UltimatumPlayer(object):
    """A generic abstract player of the ultimatum game."""

    name = "Ultimatum Player"

    def offer(self) -> float:
        """Returns a value between 0 and 1 for the proportion offered to the
        coplayer."""
        raise NotImplementedError

    def consider(self, offer: float) -> bool:
        """Decision rule for whether to accept the offer."""
        raise NotImplementedError


class SimpleThresholdPlayer(UltimatumPlayer):
    """A """

    name = "Simple Threshold Player"

    def __init__(self, offer_proportion=0.5, lower_threshold=0.5):
        self.offer_proportion = offer_proportion
        self.lower_threshold = lower_threshold

    def __repr__(self) -> str:
        return "SimpleThresholdPlayer ({} | {})".format(
            self.offer_proportion, self.lower_threshold)

    def offer(self) -> float:
        return self.offer_proportion

    def consider(self, offer: float) -> bool:
        return offer >= self.lower_threshold


class DoubleThresholdPlayer(UltimatumPlayer):
    """A generic player of the ultimatum game."""

    name = "Double Threshold Player"

    def __init__(self, offer_proportion, lower_threshold, upper_threshold):
        self.offer_proportion = offer_proportion
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def __repr__(self) -> str:
        return "DoubleThresholdPlayer ({} | [{}, {}])".format(
            self.offer_proportion,
            self.lower_threshold,
            self.upper_threshold)

    def offer(self) -> float:
        return self.offer_proportion

    def consider(self, offer: float) -> bool:
        return (offer >= self.lower_threshold) and (
            offer <= self.upper_threshold)


class DistributionPlayer(UltimatumPlayer):
    """A generic player of the ultimatum game."""

    name = "Distribution Threshold Player"

    def __init__(self, offer_distribution: None, acceptance_distribution=None):
        if not offer_distribution:
            offer_distribution = stats.norm(0.5, 0.1)
        if not acceptance_distribution:
            acceptance_distribution = stats.norm(0.5, 0.1)
        self.offer_distribution = offer_distribution
        self.acceptance_distribution = acceptance_distribution

    def __repr__(self) -> str:
        return "DistributionThresholdPlayer"

    def offer(self) -> float:
        return self.offer_proportion.rvs()

    def consider(self, offer: float) -> bool:
        return self.acceptance_distribution.rvs() <= offer


