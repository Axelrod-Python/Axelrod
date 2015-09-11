"""Tests for the hunter strategy."""

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestMetaMajority(TestPlayer):

    name = "Meta Majority"
    player = axelrod.MetaMajority
    expected_behaviour = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'manipulates_opponent_source': False,
        'inspects_opponent_source': False,
        'manipulates_opponent_state': False
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


class TestMetaMinority(TestPlayer):

    name = "Meta Minority"
    player = axelrod.MetaMinority
    expected_behaviour = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_opponent_source': False,
        'manipulates_opponent_source': False,
        'manipulates_opponent_state': False
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


class TestMetaWinner(TestPlayer):

    name = "Meta Winner"
    player = axelrod.MetaWinner
    expected_behaviour = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'inspects_opponent_source': False,
        'manipulates_opponent_source': False,
        'manipulates_opponent_state': False
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
