import numpy as np
import unittest

from axelrod.ultimatum import (
    SimpleThresholdPlayer,
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
            result[0].actions[UltimatumPosition.OFFERER], 0.6
        )
        np.testing.assert_almost_equal(
            result[0].actions[UltimatumPosition.DECIDER], True
        )
        result = coplayer.play(player)
        np.testing.assert_almost_equal(
            result[0].actions[UltimatumPosition.OFFERER], 0.5
        )
        np.testing.assert_almost_equal(
            result[0].actions[UltimatumPosition.DECIDER], True
        )
        player = SimpleThresholdPlayer(0.4, 0.6)
        result = player.play(coplayer)
        np.testing.assert_almost_equal(
            result[0].actions[UltimatumPosition.OFFERER], 0.4
        )
        np.testing.assert_almost_equal(
            result[0].actions[UltimatumPosition.DECIDER], False
        )
        result = coplayer.play(player)
        np.testing.assert_almost_equal(
            result[0].actions[UltimatumPosition.OFFERER], 0.5
        )
        np.testing.assert_almost_equal(
            result[0].actions[UltimatumPosition.DECIDER], False
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

