"""Strategy match tests."""

import axelrod as axl

from .test_player import TestMatch

C, D = axl.Action.C, axl.Action.D


class TestTFTvsWSLS(TestMatch):
    """Test TFT vs WSLS"""

    def test_rounds(self):
        self.versus_test(
            axl.TitForTat(), axl.WinStayLoseShift(), [C, C, C, C], [C, C, C, C]
        )


class TestTFTvSTFT(TestMatch):
    """Test TFT vs Suspicious TFT"""

    def test_rounds(self):
        self.versus_test(
            axl.TitForTat(),
            axl.SuspiciousTitForTat(),
            [C, D, C, D, C, D],
            [D, C, D, C, D, C],
        )


class TestTFTvsBully(TestMatch):
    """Test TFT vs Bully"""

    def test_rounds(self):
        self.versus_test(
            axl.TitForTat(), axl.Bully(), [C, D, D, C, C, D], [D, D, C, C, D, D]
        )


class TestTF2TvsBully(TestMatch):
    """Test Tit for Two Tats vs Bully"""

    def test_rounds(self):
        self.versus_test(
            axl.TitFor2Tats(),
            axl.Bully(),
            [C, C, D, D, C, C, C, D],
            [D, D, D, C, C, D, D, D],
        )


class TestZDGTFT2vsBully(TestMatch):
    """Test ZDGTFT2 vs Bully"""

    def test_rounds(self):
        self.versus_test(
            axl.ZDGTFT2(),
            axl.Bully(),
            [C, D, D, C, C, D],
            [D, D, C, C, D, D],
            seed=2,
        )


class TestZDExtort2vsTFT(TestMatch):
    """Test ZDExtort2 vs Bully"""

    def test_rounds(self):
        self.versus_test(
            axl.ZDExtort2(),
            axl.TitForTat(),
            [C, D, C, D, D, D],
            [C, C, D, C, D, D],
            seed=100,
        )


class FoolMeOncevsBully(TestMatch):
    """Test Fool Me Once vs Bully"""

    def test_rounds(self):
        self.versus_test(
            axl.FoolMeOnce(),
            axl.Bully(),
            [C, C, D, D, D, D],
            [D, D, D, C, C, C],
        )


class FoolMeOncevsSTFT(TestMatch):
    """Test Fool Me Once vs Suspicious TFT"""

    def test_rounds(self):
        self.versus_test(
            axl.FoolMeOnce(), axl.SuspiciousTitForTat(), [C] * 9, [D] + [C] * 8
        )


class GrudgervsSTFT(TestMatch):
    """Test Grudger vs Suspicious TFT"""

    def test_rounds(self):
        self.versus_test(
            axl.Grudger(),
            axl.SuspiciousTitForTat(),
            [C] + [D] * 9,
            [D, C] + [D] * 8,
        )


class TestWSLSvsBully(TestMatch):
    """Test WSLS vs Bully"""

    def test_rounds(self):
        self.versus_test(
            axl.WinStayLoseShift(),
            axl.Bully(),
            [C, D, C, C, D],
            [D, D, C, D, D],
        )
