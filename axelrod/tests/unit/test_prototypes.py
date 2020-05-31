import unittest

from axelrod.prototypes import Outcome, Position


class TestPosition(Position):
    POS_1 = 1
    POS_2 = 2
    POS_3 = 3


class TestOutcome(unittest.TestCase):
    def test_play_coplay_returns_value_error(self):
        outcome = Outcome(
            actions={TestPosition.POS_1: 1, TestPosition.POS_2: 2}
        )
        with self.assertRaises(ValueError):
            outcome.play()
        with self.assertRaises(ValueError):
            outcome.coplay()

    def test_coplay_returns_runtime_error(self):
        outcome = Outcome(
            actions={
                TestPosition.POS_1: 1,
                TestPosition.POS_2: 2,
                TestPosition.POS_3: 3,
            },
            position=TestPosition.POS_1,
        )
        with self.assertRaises(RuntimeError):
            outcome.coplay()
