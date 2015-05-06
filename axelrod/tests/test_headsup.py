"""Test for the cooperator strategy."""

import axelrod

from test_player import TestHeadsUp

C, D = 'C', 'D'


class TestTFTvsWSLS(TestHeadsUp):
    """Test TFT vs WSLS"""
    def test_rounds(self):
        outcomes = [[C, C], [C, C], [C, C], [C, C]]
        self.versus_test(axelrod.TitForTat, axelrod.WinStayLoseShift, outcomes)


class TestTFTvSTFT(TestHeadsUp):
    """Test TFT vs Suspicious TFT"""
    def test_rounds(self):
        outcomes = [[C, D], [D, C], [C, D], [D, C], [C, D], [D, C]]
        self.versus_test(
            axelrod.TitForTat, axelrod.SuspiciousTitForTat, outcomes)


class TestTFTvsBully(TestHeadsUp):
    """Test TFT vs Bully"""
    def test_rounds(self):
        outcomes = [[C, D], [D, D], [D, C], [C, C], [C, D], [D, D]]
        self.versus_test(axelrod.TitForTat, axelrod.Bully, outcomes)


class TestTF2TvsBully(TestHeadsUp):
    """Test Tit for Two Tats vs Bully"""
    def test_rounds(self):
        outcomes = [
            [C, D], [C, D], [D, D], [D, C], [C, C], [C, D], [C, D], [D, D]]
        self.versus_test(axelrod.TitFor2Tats, axelrod.Bully, outcomes)


class TestZDGTFT2vsBully(TestHeadsUp):
    """Test ZDGTFT2 vs Bully"""
    def test_rounds(self):
        outcomes = [[C, D], [D, D], [D, C], [C, C], [C, D], [D, D]]
        self.versus_test(
            axelrod.ZDGTFT2, axelrod.Bully, outcomes, random_seed=2)


class TestZDExtort2vsTFT(TestHeadsUp):
    """Test ZDExtort2 vs Bully"""
    def test_rounds(self):
        outcomes = [[C, C], [D, C], [D, D], [D, D], [D, D], [D, D]]
        self.versus_test(
            axelrod.ZDExtort2, axelrod.TitForTat, outcomes, random_seed=2)


class FoolMeOncevsBully(TestHeadsUp):
    """Test Fool Me Once vs Bully"""
    def test_rounds(self):
        outcomes = [[C, D], [C, D], [D, D], [D, C], [D, C], [D, C]]
        self.versus_test(axelrod.FoolMeOnce, axelrod.Bully, outcomes)


class FoolMeOncevsSTFT(TestHeadsUp):
    """Test Fool Me Once vs Suspicious TFT"""
    def test_rounds(self):
        outcomes = [[C, D]] + [[C, C]]*8
        self.versus_test(
            axelrod.FoolMeOnce, axelrod.SuspiciousTitForTat, outcomes)


class GrudgervsSTFT(TestHeadsUp):
    """Test Grudger vs Suspicious TFT"""
    def test_rounds(self):
        outcomes = [[C, D], [D, C]] + [[D, D]]*8
        self.versus_test(
            axelrod.Grudger, axelrod.SuspiciousTitForTat, outcomes)


class TestWSLSvsBully(TestHeadsUp):
    """Test WSLS vs Bully"""
    def test_rounds(self):
        outcomes = [[C, D], [D, D], [C, C], [C, D], [D, D]]
        self.versus_test(axelrod.WinStayLoseShift, axelrod.Bully, outcomes)
