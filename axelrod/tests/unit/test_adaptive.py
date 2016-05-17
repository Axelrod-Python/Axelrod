"""Test for the Adaptive strategy."""

import axelrod

from .test_player import TestHeadsUp, TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestAdaptive(TestPlayer):

    name = "Adaptive"
    player = axelrod.Adaptive
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Test initial play sequence
        self.responses_test([], [], [C] * 6 + [D] * 5)

    def test_scoring(self):
        player = axelrod.Adaptive()
        opponent = axelrod.Cooperator()
        player.play(opponent)
        player.play(opponent)
        self.assertEqual(3, player.scores[C])
        game = axelrod.Game(-3, 10, 10, 10)
        player.set_match_attributes(game=game)
        player.play(opponent)
        self.assertEqual(0, player.scores[C])


class TestAdaptivevsCooperator(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.Adaptive(), axelrod.Cooperator(),
                         [C] * 6 + [D] * 5 + [D] * 3, [C] * 14)

class TestAdaptivevsDefector(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.Adaptive(), axelrod.Defector(),
                         [C] * 6 + [D] * 5 + [D] * 3, [D] * 14)

class TestAdaptivevsAlternator(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.Adaptive(), axelrod.Alternator(),
                         [C] * 6 + [D] * 5 + [D] * 3, [C, D] * 7)

class TestAdaptivevsTFT(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.Adaptive(), axelrod.TitForTat(),
                         [C] * 6 + [D] * 5 + [C, C], [C] * 7 + [D] * 4 + [D, C])
