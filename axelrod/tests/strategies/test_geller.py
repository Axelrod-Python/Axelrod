"""Tests for the Geller strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestGeller(TestPlayer):

    name = "Geller"
    player = axl.Geller
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": True,  # Finds out what opponent will do
        "manipulates_state": False,
        "manipulates_source": False,
    }

    @classmethod
    def tearDownClass(cls):
        """After all tests have run, makes sure the Darwin genome is reset."""
        axl.Darwin.reset_genome()
        super(TestGeller, cls).tearDownClass()

    def setUp(self):
        """Each test starts with the basic Darwin genome."""
        axl.Darwin.reset_genome()
        super(TestGeller, self).setUp()

    def test_foil_strategy_inspection(self):
        axl.seed(2)
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)
        self.assertEqual(player.foil_strategy_inspection(), D)
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_strategy(self):
        """Should cooperate against cooperators and defect against defectors."""
        self.versus_test(axl.Defector(), expected_actions=[(D, D)] * 5)
        self.versus_test(axl.Cooperator(), expected_actions=[(C, C)] * 5)
        self.versus_test(axl.Alternator(), expected_actions=[(C, C), (D, D)] * 5)

    def test_strategy_against_lookerup_players(self):
        """
        Regression test for a bug discussed in
        https://github.com/Axelrod-Python/Axelrod/issues/1185
        """
        self.versus_test(
            axl.EvolvedLookerUp1_1_1(), expected_actions=[(C, C), (C, C)]
        )
        self.versus_test(
            axl.EvolvedLookerUp2_2_2(), expected_actions=[(C, C), (C, C)]
        )

    def test_returns_foil_inspection_strategy_of_opponent(self):
        self.versus_test(
            axl.GellerDefector(),
            expected_actions=[(D, D), (D, D), (D, C), (D, C)],
            seed=2,
        )

        self.versus_test(axl.Darwin(), expected_actions=[(C, C), (C, C), (C, C)])

        self.versus_test(
            axl.MindReader(), expected_actions=[(D, D), (D, D), (D, D)], seed=1
        )


class TestGellerCooperator(TestGeller):

    name = "Geller Cooperator"
    player = axl.GellerCooperator
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": True,  # Finds out what opponent will do
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_foil_strategy_inspection(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_returns_foil_inspection_strategy_of_opponent(self):
        self.versus_test(
            axl.GellerDefector(), expected_actions=[(D, C), (D, C), (D, C), (D, C)]
        )

        self.versus_test(axl.Darwin(), expected_actions=[(C, C), (C, C), (C, C)])

        self.versus_test(
            axl.MindReader(), expected_actions=[(D, D), (D, D), (D, D)]
        )


class TestGellerDefector(TestGeller):

    name = "Geller Defector"
    player = axl.GellerDefector
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": True,  # Finds out what opponent will do
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_foil_strategy_inspection(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)

    def test_returns_foil_inspection_strategy_of_opponent(self):

        self.versus_test(
            axl.GellerDefector(), expected_actions=[(D, D), (D, D), (D, D), (D, D)]
        )

        self.versus_test(axl.Darwin(), expected_actions=[(C, C), (C, C), (C, C)])

        self.versus_test(
            axl.MindReader(), expected_actions=[(D, D), (D, D), (D, D)]
        )
