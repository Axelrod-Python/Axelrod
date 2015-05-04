"""Test for the tit for tat strategies."""

import axelrod

from test_player import TestPlayer

C, D = 'C', 'D'

class TestTitForTat(TestPlayer):

    name = "Tit For Tat"
    player = axelrod.TitForTat

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Repeats last action of opponent history."""
        self.markov_test([C,D,C,D])
        self.responses_test([],[C,C,C,C],[C])
        self.responses_test([],[C,C,C,C,D],[D])

class TestTitFor2Tats(TestPlayer):

    name = 'Tit For 2 Tats'
    player = axelrod.TitFor2Tats

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Will defect only when last two turns of opponent were defections."""
        P1 = axelrod.TitFor2Tats()
        P2 = axelrod.Player()
        self.responses_test([C,C,C],[D,D,D],[D])
        self.responses_test([C,C,D,D],[D,D,D,C],[C])

class TestTwoTitsForTat(TestPlayer):

    name = 'Two Tits For Tat'
    player = axelrod.TwoTitsForTat

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Will defect twice when last turn of opponent was defection."""
        self.responses_test([C,C],[D,D],[D])
        self.responses_test([C,C,C],[D,D,C],[D])
        self.responses_test([C,C,D,D],[D,D,C, C],[C])

class TestBully(TestPlayer):

    name = "Bully"
    player = axelrod.Bully

    def test_strategy(self):
        """Starts by defecting"""
        self.first_play_test(D)

    def test_affect_of_strategy(self):
        """Will do opposite of what opponent does."""
        self.markov_test([D,C,D,C])

class TestSneakyTitForTat(TestPlayer):

    name = "Sneaky Tit For Tat"
    player = axelrod.SneakyTitForTat

    def test_strategy(self):
        """Starts by cooperating."""
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        """Will try defecting after two turns of cooperation, but will stop if punished."""
        self.responses_test([C,C],[C,C],[D])
        self.responses_test([C,C,D,D],[C,C,C,D],[C])

class TestSuspiciousTitForTat(TestPlayer):

    name = 'Suspicious Tit For Tat'
    player = axelrod.SuspiciousTitForTat

    def test_strategy(self):
        """Starts by Defecting"""
        self.first_play_test(D)

    def test_affect_of_strategy(self):
        """Plays like TFT after the first move, repeating the opponents last move."""
        self.markov_test([C,D,C,D])

class TestAntiTitForTat(TestPlayer):

    name = 'Anti Tit For Tat'
    player = axelrod.AntiTitForTat

    def test_strategy(self):
        """Starts by Cooperating"""
        self.first_play_test(C)

    def test_affect_of_strategy(self):
        """Will do opposite of what opponent does."""
        self.markov_test([D,C,D,C])
