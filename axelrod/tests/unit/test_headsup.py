"""Test for the cooperator strategy."""

import axelrod

from .test_player import TestHeadsUp

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestTFTvsWSLS(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        self.versus_test(axelrod.TitForTat(), axelrod.WinStayLoseShift(),
                         [C, C, C, C], [C, C, C, C])


class TestTFTvSTFT(TestHeadsUp):
    """Test TFT vs Suspicious TFT"""
    def test_rounds(self):
        self.versus_test(axelrod.TitForTat(), axelrod.SuspiciousTitForTat(),
                         [C, D, C, D, C, D], [D, C, D, C, D, C])


class TestTFTvsBully(TestHeadsUp):
    """Test TFT vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.TitForTat(), axelrod.Bully(),
                         [C, D, D, C, C, D], [D, D, C, C, D, D])


class TestTF2TvsBully(TestHeadsUp):
    """Test Tit for Two Tats vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.TitFor2Tats(), axelrod.Bully(),
                         [C, C, D, D, C, C, C, D], [D, D, D, C, C, D, D, D])


class TestZDGTFT2vsBully(TestHeadsUp):
    """Test ZDGTFT2 vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.ZDGTFT2(), axelrod.Bully(), [C, D, D, C, C, D],
            [D, D, C, C, D, D], random_seed=2)


class TestZDExtort2vsTFT(TestHeadsUp):
    """Test ZDExtort2 vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.ZDExtort2(), axelrod.TitForTat(),
                         [C, D, D, D, D, D], [C, C, D, D, D, D], random_seed=2)


class FoolMeOncevsBully(TestHeadsUp):
    """Test Fool Me Once vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.FoolMeOnce(), axelrod.Bully(),
                         [C, C, D, D, D, D], [D, D, D, C, C, C])


class FoolMeOncevsSTFT(TestHeadsUp):
    """Test Fool Me Once vs Suspicious TFT"""
    def test_rounds(self):
        self.versus_test(axelrod.FoolMeOnce(), axelrod.SuspiciousTitForTat(),
                         [C] * 9, [D] + [C] * 8)


class GrudgervsSTFT(TestHeadsUp):
    """Test Grudger vs Suspicious TFT"""
    def test_rounds(self):
        self.versus_test(axelrod.Grudger(), axelrod.SuspiciousTitForTat(),
                         [C] + [D] * 9, [D, C] + [D] * 8)


class TestWSLSvsBully(TestHeadsUp):
    """Test WSLS vs Bully"""
    def test_rounds(self):
        self.versus_test(axelrod.WinStayLoseShift(), axelrod.Bully(),
                         [C, D, C, C, D], [D, D, C, D, D])
