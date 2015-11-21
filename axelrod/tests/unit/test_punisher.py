"""Test for the punisher strategy."""

import random

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestPunisher(TestPlayer):

    name = "Punisher"
    player = axelrod.Punisher
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        """Tests for the __init__ method."""
        P1 = axelrod.Punisher()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.mem_length, 1)
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 1)

    def test_strategy(self):
        self.responses_test([], [], [C], attrs={"grudged": False})
        self.responses_test([C], [C], [C], attrs={"grudged": False})
        self.responses_test([C], [D], [D], attrs={"grudged": True})
        for i in range(10):
            self.responses_test([C, C] + [D] * i, [C, D] + [C] * i, [D],
                                attrs={"grudged": True, "grudge_memory": i,
                                       "mem_length": 10})
        # Eventually the grudge is dropped
        i = 11
        self.responses_test([C, C] + [D] * i, [C, D] + [C] * i, [C],
                            attrs={"grudged": False, "grudge_memory": 0,
                                    "mem_length": 10})

        # Grudged again on opponent's D
        self.responses_test([C, C] + [D] * i + [C], [C, D] + [C] * i + [D], [D],
                            attrs={"grudged": True, "grudge_memory": 0,
                                   "mem_length": 2})

    def test_reset_method(self):
        """Tests the reset method."""
        P1 = axelrod.Punisher()
        P1.history = [C, D, D, D]
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)


class TestInversePunisher(TestPlayer):

    name = "Inverse Punisher"
    player = axelrod.InversePunisher
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_init(self):
        """Tests for the __init__ method."""
        P1 = axelrod.InversePunisher()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.mem_length, 1)
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 1)

    def test_strategy(self):
        self.responses_test([], [], [C], attrs={"grudged": False})
        self.responses_test([C], [C], [C], attrs={"grudged": False})
        self.responses_test([C], [D], [D], attrs={"grudged": True})
        for i in range(10):
            self.responses_test([C, C] + [D] * i, [C, D] + [C] * i, [D],
                                attrs={"grudged": True, "grudge_memory": i,
                                       "mem_length": 10})
        # Eventually the grudge is dropped
        i = 11
        self.responses_test([C, C] + [D] * i, [C, D] + [C] * i, [C],
                            attrs={"grudged": False, "grudge_memory": 0,
                                    "mem_length": 10})
        # Grudged again on opponent's D
        self.responses_test([C, C] + [D] * i + [C], [C, D] + [C] * i + [D], [D],
                            attrs={"grudged": True, "grudge_memory": 0,
                                   "mem_length": 17})

        # Test a different grudge length period
        self.responses_test([C] * 5, [C] * 4 + [D],
                            [D], attrs={"grudged": True, "grudge_memory": 0,
                                        "mem_length": 16})

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.InversePunisher()
        P1.history = [C, D, D, D]
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)
