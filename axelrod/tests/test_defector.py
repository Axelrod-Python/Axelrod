"""Test for the defector strategy."""

import axelrod

from test_player import TestPlayer, C, D


class TestDefector(TestPlayer):

    name = "Defector"
    player = axelrod.Defector
    stoachastic = False

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):
        """Test that always defects."""
        self.markov_test([D,D,D,D])

class TestTrickyDefector(TestPlayer):

    name = "Tricky Defector"
    player = axelrod.TrickyDefector
    stochastic = False

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):
        """Test if it tries to trick opponent"""
        self.markov_test([D,D,D,D])
        self.responses_test([C,C,C],[C,C,C],[D])
        self.responses_test([C,C,C,D,D],[C,C,C,C,D],[D])
        self.responses_test([C,C,C,D,D]+[C]*11,[C,C,C,C,D]+[D] + [C]*10,[D])
