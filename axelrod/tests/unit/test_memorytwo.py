"""Tests for the Memorytwo strategies."""

import axelrod
from .test_player import TestPlayer


C, D = axelrod.Actions.C, axelrod.Actions.D


class TestMEM2(TestPlayer):

    name = "MEM2"
    player = axelrod.MEM2
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Start with TFT
        self.responses_test([C])
        self.responses_test([C], [C], [C])
        self.responses_test([D], [C], [D])
        # TFT if mutual cooperation on first two rounds
        self.responses_test([C], [C, C], [C, C])
        self.responses_test([D], [C, D], [D, D])
        # TFTT if C, D and D, C
        self.responses_test([C], [C, C, C, D], [C, C, D, C])
        self.responses_test([D], [C, C, C, D, C, D], [C, C, D, C, D, D])
        # TFTT if D, C and C, D
        self.responses_test([C], [C, C, D, C], [C, D, C, D])
        self.responses_test([D], [C, C, D, C, C, D], [C, C, D, C, D, D])
        # ALLD Otherwise
        self.responses_test([D], [C, D], [D, D])
        self.responses_test([D], [C, D, D], [D, D, D])
        # ALLD forever if all D twice
        self.responses_test([D] * 10, [C, D, D, D, D, D], [D, D, D, D, D, D])
        self.responses_test([D] * 9, [C] + [D] * 5 + [C] * 4, [D] * 6 + [C] * 4)

    def attribute_equality_test(self, player, clone):
        """Overwrite specific test to be able to test self.players"""
        for p in [player, clone]:
            self.assertEqual(p.play_as, "TFT")
            self.assertEqual(p.shift_counter, 3)
            self.assertEqual(p.alld_counter, 0)

        for key, value in [("TFT", axelrod.TitForTat),
                           ("TFTT", axelrod.TitFor2Tats),
                           ("ALLD", axelrod.Defector)]:
            self.assertEqual(p.players[key].history, [])
            self.assertIsInstance(p.players[key], value)
