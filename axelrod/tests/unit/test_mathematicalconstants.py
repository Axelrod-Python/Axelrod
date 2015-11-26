"""Test for the golden and other mathematical strategies."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGolden(TestPlayer):

    name = '$\phi$'
    player = axelrod.Golden
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """test initial strategy co-operates"""
        self.first_play_test(C)

    def test_when_no_defection(self):
        """tests that if the opposing player does not defect initially then strategy defects"""
        self.responses_test([C], [C], [D])

    def test_when_greater_than_golden_ratio(self):
        """tests that if the ratio of Cs to Ds is greater than the golden ratio then strategy defects"""
        self.responses_test([C] * 4, [C, C, D, D], [D])

    def test_when_less_than_golder_ratio(self):
        """tests that if the ratio of Cs to Ds is less than the golden ratio then strategy co-operates"""
        self.responses_test([C] * 4, [D] * 4, [C])


class TestPi(TestPlayer):

    name = '$\pi$'
    player = axelrod.Pi
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """test initial strategy co-operates"""
        self.first_play_test(C)

    def test_when_no_defection(self):
        """tests that if the opposing player does not defect initially then strategy defects"""
        self.responses_test([C], [C], [D])

    def test_when_greater_than_pi(self):
        """tests that if the ratio of Cs to Ds is greater than pi then strategy defects"""
        self.responses_test([C] * 4, [C, C, C, D], [D])

    def test_when_less_than_pi(self):
        """tests that if the ratio of Cs to Ds is less than pi then strategy co-operates"""
        self.responses_test([C] * 4, [C, C, D, D], [C])


class Teste(TestPlayer):

    name = '$e$'
    player = axelrod.e
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """test initial strategy co-operates"""
        self.first_play_test(C)

    def test_when_no_defection(self):
        """tests that if the opposing player does not defect initially then strategy defects"""
        self.responses_test([C], [C], [D])

    def test_when_greater_than_e(self):
        """tests that if the ratio of Cs to Ds is greater than e then strategy defects"""
        self.responses_test([C] * 4, [C, C, D, D], [D])

    def test_when_less_than_e(self):
        """tests that if the ratio of Cs to Ds is less than e then strategy co-operates"""
        self.responses_test([C] * 4, [C, D, D, D], [C])
