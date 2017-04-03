"""Tests for the Geller strategy."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGeller(TestPlayer):

    name = "Geller"
    player = axelrod.Geller
    expected_classifier = {
        'memory_depth': -1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_state': False,
        'manipulates_source': False
    }

    def test_foil_strategy_inspection(self):
        axelrod.seed(2)
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)
        self.assertEqual(player.foil_strategy_inspection(), D)
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_strategy(self):
        """Should cooperate against cooperators and defect against defectors."""
        self.versus_test(axelrod.Defector(), expected_actions=[(D, D)] * 5)
        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)] * 5)
        self.versus_test(axelrod.Alternator(), expected_actions=[(C, C), (D, D)] * 5)

    def test_returns_foil_inspection_strategy_of_opponent(self):
        seed = 2
        # each Geller type returns the other's foil_inspection_strategy
        self.versus_test(axelrod.GellerDefector(), expected_actions=[(D, D), (D, D), (D, C), (D, C)], seed=seed)

        self.versus_test(axelrod.Darwin(), expected_actions=[(C, C), (C, C), (C, C)])

        self.versus_test(axelrod.MindReader(), expected_actions=[(D, D), (D, C), (D, D)], seed=seed)


class TestGellerCooperator(TestGeller):

    name = "Geller Cooperator"
    player = axelrod.GellerCooperator
    expected_classifier = {
        'memory_depth': -1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_foil_strategy_inspection(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_returns_foil_inspection_strategy_of_opponent(self):
        self.versus_test(axelrod.GellerDefector(), expected_actions=[(D, C), (D, C), (D, C), (D, C)])

        self.versus_test(axelrod.Darwin(), expected_actions=[(C, C), (C, C), (C, C)])

        self.versus_test(axelrod.MindReader(), expected_actions=[(D, D), (D, D), (D, D)])


class TestGellerDefector(TestGeller):

    name = "Geller Defector"
    player = axelrod.GellerDefector
    expected_classifier = {
        'memory_depth': -1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_foil_strategy_inspection(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)

    def test_returns_foil_inspection_strategy_of_opponent(self):
        self.versus_test(axelrod.GellerDefector(), expected_actions=[(D, D), (D, D), (D, D), (D, D)])

        self.versus_test(axelrod.Darwin(), expected_actions=[(C, C), (C, C), (C, C)])

        self.versus_test(axelrod.MindReader(), expected_actions=[(D, D), (D, D), (D, D)])
