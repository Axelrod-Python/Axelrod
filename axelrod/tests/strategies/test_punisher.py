"""Tests for the Punisher strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestPunisher(TestPlayer):

    name = "Punisher"
    player = axelrod.Punisher
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
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
        self.responses_test([C], [], [], attrs={"grudged": False})
        self.responses_test([C], [C], [C], attrs={"grudged": False})
        self.responses_test([D], [C], [D], attrs={"grudged": True})
        for i in range(10):
            self.responses_test([D], [C, C] + [D] * i, [C, D] + [C] * i,
                                attrs={"grudged": True, "grudge_memory": i,
                                       "mem_length": 10})
        # Eventually the grudge is dropped
        i = 11
        self.responses_test([C], [C, C] + [D] * i, [C, D] + [C] * i,
                            attrs={"grudged": False, "grudge_memory": 0,
                                   "mem_length": 10})

        # Grudged again on opponent's D
        self.responses_test([D], [C, C] + [D] * i + [C], [C, D] + [C] * i + [D],
                            attrs={"grudged": True, "grudge_memory": 0,
                                   "mem_length": 2})


class TestInversePunisher(TestPlayer):

    name = "Inverse Punisher"
    player = axelrod.InversePunisher
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic' : False,
        'makes_use_of': set(),
        'long_run_time': False,
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
        self.responses_test([C], [], [], attrs={"grudged": False})
        self.responses_test([C], [C], [C], attrs={"grudged": False})
        self.responses_test([D], [C], [D], attrs={"grudged": True})
        for i in range(10):
            self.responses_test([D], [C, C] + [D] * i, [C, D] + [C] * i,
                                attrs={"grudged": True, "grudge_memory": i,
                                       "mem_length": 10})
        # Eventually the grudge is dropped
        i = 11
        self.responses_test([C], [C, C] + [D] * i, [C, D] + [C] * i,
                            attrs={"grudged": False, "grudge_memory": 0,
                                   "mem_length": 10})
        # Grudged again on opponent's D
        self.responses_test([D], [C, C] + [D] * i + [C], [C, D] + [C] * i + [D],
                            attrs={"grudged": True, "grudge_memory": 0,
                                   "mem_length": 17})

        # Test a different grudge length period
        self.responses_test([D], [C] * 5, [C] * 4 + [D],
                            attrs={"grudged": True, "grudge_memory": 0,
                                   "mem_length": 16})

class TestLevelPunisher(TestPlayer):

    name = "Level Punisher"
    player = axelrod.LevelPunisher
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by Cooperating
        self.first_play_test(C)

        # Defects if the turns played are less than 10.
        self.responses_test([C], [C], [C])
        self.responses_test([C], [C] * 4, [C, D, C, D])

        # Check for the number of rounds greater than 10.
        self.responses_test([C], [C] * 10, [C, C, C, C, D, C, C, C, C, D])
        #Check if number of defections by opponent is greater than 20%
        self.responses_test([D], [C] * 10, [D, D, D, D, D, C, D, D, D, D])
