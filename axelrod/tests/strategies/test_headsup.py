"""Strategy match tests."""

import axelrod
from .test_player import TestMatch

C, D = axelrod.Action.C, axelrod.Action.D


class TestTFTvsWSLS(TestMatch):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.TitForTat(), axelrod.WinStayLoseShift(),
                         [C, C, C, C], [C, C, C, C])


class TestTFTvSTFT(TestMatch):
    """Test TFT vs Suspicious TFT"""
    def test_rounds(self):
        self.versus_test(axelrod.TitForTat(), axelrod.SuspiciousTitForTat(),
                         [C, D, C, D, C, D], [D, C, D, C, D, C])


class TestTFTvsBully(TestMatch):
    """Test TFT vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.TitForTat(), axelrod.Bully(),
                         [C, D, D, C, C, D], [D, D, C, C, D, D])


class TestTF2TvsBully(TestMatch):
    """Test Tit for Two Tats vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.TitFor2Tats(), axelrod.Bully(),
                         [C, C, D, D, C, C, C, D], [D, D, D, C, C, D, D, D])


class TestZDGTFT2vsBully(TestMatch):
    """Test ZDGTFT2 vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.ZDGTFT2(), axelrod.Bully(), [C, D, D, C, C, C],
            [D, D, C, C, D, D], seed=2)


class TestZDExtort2vsTFT(TestMatch):
    """Test ZDExtort2 vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.ZDExtort2(), axelrod.TitForTat(),
                         [C, D, D, D, D, D], [C, C, D, D, D, D], seed=2)


class FoolMeOncevsBully(TestMatch):
    """Test Fool Me Once vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.FoolMeOnce(), axelrod.Bully(),
                         [C, C, D, D, D, D], [D, D, D, C, C, C])


class FoolMeOncevsSTFT(TestMatch):
    """Test Fool Me Once vs Suspicious TFT"""
    def test_rounds(self):
        self.versus_test(axelrod.FoolMeOnce(), axelrod.SuspiciousTitForTat(),
                         [C] * 9, [D] + [C] * 8)


class GrudgervsSTFT(TestMatch):
    """Test Grudger vs Suspicious TFT"""
    def test_rounds(self):
        self.versus_test(axelrod.Grudger(), axelrod.SuspiciousTitForTat(),
                         [C] + [D] * 9, [D, C] + [D] * 8)


class TestWSLSvsBully(TestMatch):
    """Test WSLS vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.WinStayLoseShift(), axelrod.Bully(),
                         [C, D, C, C, D], [D, D, C, D, D])
