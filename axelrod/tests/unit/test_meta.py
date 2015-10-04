"""Tests for the hunter strategy."""

import random

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestMetaMajority(TestPlayer):

    name = "Meta Majority"
    player = axelrod.MetaMajority
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'manipulates_source': False,
        'inspects_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        P1 = axelrod.MetaMajority()
        P2 = axelrod.Player()

        # With more cooperators on the team than defectors, we should cooperate.
        P1.team = [axelrod.Cooperator(), axelrod.Cooperator(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), C)

        # With more defectors, we should defect.
        P1.team = [axelrod.Cooperator(), axelrod.Defector(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), D)

    def test_reset(self):
        p1 = self.player()
        p2 = axelrod.Cooperator()
        p1.play(p2)
        p1.play(p2)
        p1.play(p2)
        p1.reset()
        for player in p1.team:
            self.assertEqual(len(player.history), 0)


class TestMetaMinority(TestPlayer):

    name = "Meta Minority"
    player = axelrod.MetaMinority
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        P1 = axelrod.MetaMinority()
        P2 = axelrod.Player()

        # With more cooperators on the team, we should defect.
        P1.team = [axelrod.Cooperator(), axelrod.Cooperator(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), D)

        # With defectors in the majority, we will cooperate here.
        P1.team = [axelrod.Cooperator(), axelrod.Defector(), axelrod.Defector()]
        self.assertEqual(P1.strategy(P2), C)

    def test_reset(self):
        p1 = self.player()
        p2 = axelrod.Cooperator()
        p1.play(p2)
        p1.play(p2)
        p1.play(p2)
        p1.reset()
        for player in p1.team:
            self.assertEqual(len(player.history), 0)


class TestMetaWinner(TestPlayer):

    name = "Meta Winner"
    player = axelrod.MetaWinner
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        P1 = axelrod.MetaWinner(team = [axelrod.Cooperator, axelrod.Defector])
        P2 = axelrod.Player()

        # This meta player will simply choose the strategy with the highest current score.
        P1.team[0].score = 0
        P1.team[1].score = 1
        self.assertEqual(P1.strategy(P2), C)
        P1.team[0].score = 1
        P1.team[1].score = 0
        self.assertEqual(P1.strategy(P2), D)

        # If there is a tie, choose to cooperate if possible.
        P1.team[0].score = 1
        P1.team[1].score = 1
        self.assertEqual(P1.strategy(P2), C)

    def test_reset(self):
        p1 = self.player()
        p2 = axelrod.Cooperator()
        p1.play(p2)
        p1.play(p2)
        p1.play(p2)
        p1.reset()
        for player in p1.team:
            self.assertEqual(len(player.history), 0)


class TestMetaHunter(TestPlayer):

    name = "Meta Hunter"
    player = axelrod.MetaHunter
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)

        # We are not using the Cooperator Hunter here, so this should lead to cooperation.
        self.responses_test([C, C, C, C], [C, C, C, C], [C])

        # After long histories tit-for-tat should come into play.
        self.responses_test([C] * 101, [C] * 100 + [D], [D])

        # All these others, however, should trigger a defection for the hunter.
        self.responses_test([C] * 4, [D] * 4, [D])
        self.responses_test([C] * 6, [C, D] * 3, [D])
        self.responses_test([C] * 8, [C, C, C, D, C, C, C, D], [D])
        self.responses_test([C] * 100, [random.choice([C, D]) for i in range(100)],[D])

    def test_reset(self):
        p1 = self.player()
        p2 = axelrod.Cooperator()
        p1.play(p2)
        p1.play(p2)
        p1.play(p2)
        p1.reset()
        for player in p1.team:
            self.assertEqual(len(player.history), 0)