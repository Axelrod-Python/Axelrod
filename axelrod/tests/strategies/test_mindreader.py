"""Tests for the Mindreader strategy."""

import axelrod as axl
from axelrod._strategy_utils import simulate_match

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestMindReader(TestPlayer):

    name = "Mind Reader"
    player = axl.MindReader
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": True,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_foil_inspection_strategy(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)

    def test_strategy(self):
        """
        Will defect against nice strategies
        """
        p1 = axl.MindReader()
        p2 = axl.Cooperator()
        self.assertEqual(p1.strategy(p2), D)

    def test_vs_defect(self):
        """
        Will defect against pure defecting strategies
        """
        p1 = axl.MindReader()
        p2 = axl.Defector()
        self.assertEqual(p1.strategy(p2), D)

    def test_vs_grudger(self):
        """
        Will keep nasty strategies happy if it can
        """
        p1 = axl.MindReader()
        p2 = axl.Grudger()
        self.assertEqual(p1.strategy(p2), C)

    def test_vs_tit_for_tat(self):
        """
        Will keep nasty strategies happy if it can
        """
        p1 = axl.MindReader()
        p2 = axl.TitForTat()
        self.assertEqual(p1.strategy(p2), C)

    def test_simulate_matches(self):
        """
        Simulates a number of matches
        """
        p1 = axl.MindReader()
        p2 = axl.Grudger()
        simulate_match(p1, p2, C, 4)
        self.assertEqual(p2.history, [C, C, C, C])

    def test_history_is_same(self):
        """
        Checks that the history is not altered by the player
        """
        p1 = axl.MindReader()
        p2 = axl.Grudger()
        p1.history.append(C, C)
        p1.history.append(C, D)
        p2.history.append(C, C)
        p2.history.append(D, C)
        p1.strategy(p2)
        self.assertEqual(p1.history, [C, C])
        self.assertEqual(p2.history, [C, D])

    def test_vs_geller(self):
        """Ensures that a recursion error does not occur """
        p1 = axl.MindReader()
        p2 = axl.Geller()
        p1.strategy(p2)
        p2.strategy(p1)

    def test_init(self):
        """Tests for init method """
        p1 = axl.MindReader()
        self.assertEqual(p1.history, [])


class TestProtectedMindReader(TestPlayer):

    name = "Protected Mind Reader"
    player = axl.ProtectedMindReader
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": True,  # Finds out what opponent will do
        "manipulates_source": True,  # Stops opponent's strategy
        "manipulates_state": False,
    }

    def test_foil_inspection_strategy(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)

    def test_strategy(self):
        """
        Will defect against nice strategies
        """
        p1 = axl.ProtectedMindReader()
        p2 = axl.Cooperator()
        self.assertEqual(p1.strategy(p2), D)

    def test_vs_defect(self):
        """
        Will defect against pure defecting strategies
        """
        p1 = axl.ProtectedMindReader()
        p2 = axl.Defector()
        self.assertEqual(p1.strategy(p2), D)

    def tests_protected(self):
        """Ensures that no other player can alter its strategy """

        p1 = axl.ProtectedMindReader()
        p2 = axl.MindController()
        P3 = axl.Cooperator()
        p2.strategy(p1)
        self.assertEqual(p1.strategy(P3), D)


class TestMirrorMindReader(TestPlayer):

    name = "Mirror Mind Reader"
    player = axl.MirrorMindReader
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": True,  # reading and copying the source of the component
        "manipulates_source": True,  # changing own source dynamically
        "manipulates_state": False,
    }

    def test_foil_inspection_strategy(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_strategy(self):
        p1 = axl.MirrorMindReader()
        p2 = axl.Cooperator()
        self.assertEqual(p1.strategy(p2), C)

    def test_vs_defector(self):
        p1 = axl.MirrorMindReader()
        p2 = axl.Defector()
        self.assertEqual(p1.strategy(p2), D)

    def test_nice_with_itself(self):
        p1 = axl.MirrorMindReader()
        p2 = axl.MirrorMindReader()
        self.assertEqual(p1.strategy(p2), C)
