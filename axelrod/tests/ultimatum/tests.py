import numpy as np
import random
from typing import List, Optional
import unittest

from scipy import stats

from axelrod.ultimatum import (
    AcceptanceThresholdPlayer,
    BinarySearchOfferPlayer,
    DistributionPlayer,
    DoubleThresholdsPlayer,
    RejectionLiftPlayer,
    SimpleThresholdPlayer,
    TitForTatDecisionPlayer,
    TitForTatOfferPlayer,
    UltimatumPlayer,
    UltimatumPosition,
)


class TestBaseUltimatumPlayer(unittest.TestCase):
    def test_unimplemented_errors(self):
        player = UltimatumPlayer()
        with self.assertRaises(NotImplementedError):
            player.offer()
        with self.assertRaises(NotImplementedError):
            player.consider(0.5)

    def test_reset_player(self):
        player1 = SimpleThresholdPlayer(0.6, 0.4)
        player2 = SimpleThresholdPlayer(0.6, 0.4)
        player1.play(player2)
        self.assertEqual(len(player1.history), 1)
        self.assertEqual(len(player2.history), 1)
        player1.reset()
        self.assertEqual(len(player1.history), 0)
        self.assertEqual(len(player2.history), 1)


class TestPlay(unittest.TestCase):
    def test_play(self):
        player = SimpleThresholdPlayer(0.6, 0.4)
        coplayer = SimpleThresholdPlayer(0.5, 0.5)
        result = player.play(coplayer)
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.OFFERER], 0.4
        )
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.DECIDER], 0.6
        )
        result = coplayer.play(player)
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.OFFERER], 0.5
        )
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.DECIDER], 0.5
        )
        player = SimpleThresholdPlayer(0.4, 0.6)
        result = player.play(coplayer)
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.OFFERER], 0.0
        )
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.DECIDER], 0.0
        )
        result = coplayer.play(player)
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.OFFERER], 0.0
        )
        np.testing.assert_almost_equal(
            result[0].scores[UltimatumPosition.DECIDER], 0.0
        )

        # Check history
        self.assertEqual(len(coplayer.history), 4)
        self.assertEqual(
            coplayer.history[0].actions[UltimatumPosition.DECIDER], True
        )
        self.assertEqual(
            coplayer.history[1].actions[UltimatumPosition.DECIDER], True
        )
        self.assertEqual(
            coplayer.history[2].actions[UltimatumPosition.DECIDER], False
        )
        self.assertEqual(
            coplayer.history[3].actions[UltimatumPosition.DECIDER], False
        )

        self.assertEqual(len(coplayer.history.offers), 2)
        self.assertEqual(
            coplayer.history.offers[0].actions[UltimatumPosition.DECIDER], True
        )
        self.assertEqual(
            coplayer.history.offers[1].actions[UltimatumPosition.DECIDER], False
        )

        self.assertEqual(len(coplayer.history.decisions), 2)
        self.assertEqual(
            coplayer.history.decisions[0].actions[UltimatumPosition.DECIDER],
            True,
        )
        self.assertEqual(
            coplayer.history.decisions[1].actions[UltimatumPosition.DECIDER],
            False,
        )


class TestSimpleThresholdPlayer(unittest.TestCase):
    def test_consider(self):
        player = SimpleThresholdPlayer(0.6, 0.4)
        self.assertFalse(player.consider(0.39))
        self.assertTrue(player.consider(0.4))
        self.assertTrue(player.consider(0.41))

    def test_offer(self):
        player = SimpleThresholdPlayer(0.4, 0.6)
        self.assertAlmostEqual(player.offer(), 0.4)

    def test_repr(self):
        player = SimpleThresholdPlayer(0.6, 0.4)
        self.assertEqual(str(player), "SimpleThresholdPlayer (0.6 | 0.4)")


class TestAcceptanceThresholdPlayer(unittest.TestCase):
    def test_consider(self):
        player = AcceptanceThresholdPlayer(0.1, 0.4, 0.6)
        self.assertFalse(player.consider(0.39))
        self.assertTrue(player.consider(0.4))
        self.assertTrue(player.consider(0.5))
        self.assertTrue(player.consider(0.6))
        self.assertFalse(player.consider(0.61))

    def test_offer(self):
        player = AcceptanceThresholdPlayer(0.1, 0.4, 0.6)
        self.assertAlmostEqual(player.offer(), 0.1)

    def test_repr(self):
        player = AcceptanceThresholdPlayer(0.1, 0.4, 0.6)
        self.assertEqual(
            str(player), "AcceptanceThresholdPlayer (0.1 | [0.4, 0.6])"
        )


class TestDoubleThresholdsPlayer(unittest.TestCase):
    def test_consider(self):
        player = DoubleThresholdsPlayer(0.4, 0.6, 0.4, 0.6)
        self.assertFalse(player.consider(0.39))
        self.assertTrue(player.consider(0.4))
        self.assertTrue(player.consider(0.41))
        self.assertTrue(player.consider(0.6))
        self.assertFalse(player.consider(0.61))

    def test_offer(self):
        a = random.random()
        b = random.uniform(a, 1)
        player = DoubleThresholdsPlayer(a, b, 0.0, 1.0)
        for _ in range(10):
            offer = player.offer()
            self.assertTrue(a <= offer <= b)

    def test_repr(self):
        player = DoubleThresholdsPlayer(0.4, 0.6, 0.4, 0.6)
        self.assertEqual(
            str(player), "DoubleThresholdsPlayer (0.4, 0.6 | [0.4, 0.6])"
        )


class MockRVContinuous(stats.distributions.rv_continuous):
    """Creates a mock distribution which returns values from the list provided
    at initialization."""

    def __init__(self, values: Optional[List[float]] = None):
        if not values:
            values = []
        self.values = values

    def rvs(self) -> float:
        if not self.values:  # pragma: no cover
            return 0.0
        result = self.values[0]
        self.values = self.values[1:]
        return result


class TestDistributionPlayer(unittest.TestCase):
    def test_consider(self):
        player = DistributionPlayer(
            MockRVContinuous(), MockRVContinuous([0.1, 0.2, 0.3, 0.4])
        )
        self.assertTrue(player.consider(0.15))
        self.assertFalse(player.consider(0.15))
        self.assertFalse(player.consider(0.25))
        self.assertTrue(player.consider(0.5))

    def test_offer(self):
        player = DistributionPlayer(
            MockRVContinuous([0.1, 0.2]), MockRVContinuous()
        )
        self.assertAlmostEqual(player.offer(), 0.1)
        self.assertAlmostEqual(player.offer(), 0.2)

    def test_repr(self):
        player = DistributionPlayer(MockRVContinuous(), MockRVContinuous())
        self.assertEqual(str(player), "DistributionThresholdPlayer")


class TestBinarySearchOfferPlayer(unittest.TestCase):
    def test_consider(self):
        player = BinarySearchOfferPlayer(0.4, 0.6)
        self.assertFalse(player.consider(0.39))
        self.assertTrue(player.consider(0.4))
        self.assertTrue(player.consider(0.5))
        self.assertTrue(player.consider(0.6))
        self.assertFalse(player.consider(0.61))

    def test_offer(self):
        player = BinarySearchOfferPlayer(0.4, 0.6)
        never_accepts = SimpleThresholdPlayer(0.5, 1.0)
        player.play(never_accepts)
        self.assertAlmostEqual(player.offer_size, 1.0 / 2)
        player.play(never_accepts)
        self.assertAlmostEqual(player.offer_size, 3.0 / 4)
        player.play(never_accepts)
        self.assertAlmostEqual(player.offer_size, 7.0 / 8)

        player = BinarySearchOfferPlayer(0.4, 0.6)
        always_accepts = SimpleThresholdPlayer(0.5, 0.0)
        player.play(always_accepts)
        self.assertAlmostEqual(player.offer_size, 1.0 / 2)
        player.play(always_accepts)
        self.assertAlmostEqual(player.offer_size, 1.0 / 4)
        player.play(always_accepts)
        self.assertAlmostEqual(player.offer_size, 1.0 / 8)

        player = BinarySearchOfferPlayer(0.4, 0.6)
        accepts_one_third = SimpleThresholdPlayer(0.5, 0.33)
        player.play(accepts_one_third)
        self.assertAlmostEqual(player.offer_size, 1.0 / 2)
        player.play(accepts_one_third)
        self.assertAlmostEqual(player.offer_size, 1.0 / 4)
        player.play(accepts_one_third)
        self.assertAlmostEqual(player.offer_size, 3.0 / 8)

    def test_repr(self):
        player = BinarySearchOfferPlayer(0.4, 0.6)
        self.assertEqual(str(player), "BinarySearchOfferPlayer [0.4, 0.6]")


class TestTitForTatOfferPlayer(unittest.TestCase):
    def test_offer(self):
        player = TitForTatOfferPlayer(default_offer=0.5)
        coplayer = SimpleThresholdPlayer(offer_proportion=0.2)
        player.play(coplayer)
        self.assertAlmostEqual(
            player.history[-1].actions[UltimatumPosition.OFFERER], 0.5
        )  # Default offer
        coplayer.play(player)  # Plays 0.2
        player.play(coplayer)
        self.assertAlmostEqual(
            player.history[-1].actions[UltimatumPosition.OFFERER], 0.2
        )  # Imitates coplayer's offer

    def test_repr(self):
        player = TitForTatOfferPlayer(0.4, 0.6, 0.8)
        self.assertEqual(str(player), "TitForTatOfferPlayer (0.4 | [0.6, 0.8])")


class TestTitForTatDecisionPlayer(unittest.TestCase):
    def test_offer(self):
        player = TitForTatDecisionPlayer(default_acceptance=True)
        never_accepts = SimpleThresholdPlayer(0.5, 1.0)
        never_accepts.play(player)
        self.assertTrue(
            player.history[-1].actions[UltimatumPosition.DECIDER]
        )  # Default decision
        player.play(never_accepts)  # Rejects decisions
        never_accepts.play(player)
        self.assertFalse(
            player.history[-1].actions[UltimatumPosition.DECIDER]
        )  # Imitate's coplayer decision

    def test_repr(self):
        player = TitForTatDecisionPlayer(0.9, False)
        self.assertEqual(str(player), "TitForTatDecisionPlayer (0.9, False)")


class TestRejectionLiftPlayer(unittest.TestCase):
    def test_offer(self):
        player = RejectionLiftPlayer()
        binary_search_player = BinarySearchOfferPlayer()

        # Weight all future turns with a total of weight 9.0.  When playing
        # against the binary player should accept when (n-1)/n > 9/n, which
        # happens for the first time when n=16.
        self.assertAlmostEqual(player.future_weight, 9.0)

        # Reject first two offers
        binary_search_player.play(player)
        self.assertFalse(player.history[-1].actions[UltimatumPosition.DECIDER])
        binary_search_player.play(player)
        self.assertFalse(player.history[-1].actions[UltimatumPosition.DECIDER])

        # Lift is estimated at 1/4
        binary_search_player.play(player)
        self.assertFalse(player.history[-1].actions[UltimatumPosition.DECIDER])

        # Lift is estimated at 1/8
        binary_search_player.play(player)
        self.assertFalse(player.history[-1].actions[UltimatumPosition.DECIDER])

        # Lift is estimated at 1/16.  Accept.
        binary_search_player.play(player)
        self.assertTrue(player.history[-1].actions[UltimatumPosition.DECIDER])

        # Continue accepting from here on.
        binary_search_player.play(player)
        self.assertTrue(player.history[-1].actions[UltimatumPosition.DECIDER])
        binary_search_player.play(player)
        self.assertTrue(player.history[-1].actions[UltimatumPosition.DECIDER])

    def test_repr(self):
        player = RejectionLiftPlayer(0.9, False)
        self.assertEqual(str(player), "RejectionLiftPlayer (0.9, False)")
