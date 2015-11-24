"""Test for the once bitten strategy."""

import random

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestOnceBitten(TestPlayer):

    name = "Once Bitten"
    player = axelrod.OnceBitten
    expected_classifier = {
        'memory_depth': 12,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """If opponent defects at any point then the player will defect
        forever."""
        # Become grudged if the opponent defects twice in a row
        self.responses_test([], [], [C], attrs={"grudged": False})
        self.responses_test([C], [C], [C], attrs={"grudged": False})
        self.responses_test([C, C], [C, C], [C], attrs={"grudged": False})
        self.responses_test([C, C, C], [C, C, D], [C], attrs={"grudged": False})
        self.responses_test([C, C, C, C], [C, C, D, D], [D],
                            attrs={"grudged": True})

        mem_length = self.player().mem_length
        for i in range(mem_length - 1):
            self.responses_test([C, C, C, C] + [D] * i, [C, C, D, D] + [D] * i,
                                [D], attrs={"grudged": True,
                                            "grudge_memory": i})
        i = mem_length + 1
        self.responses_test([C, C, C, C] + [D] * i, [C, C, D, D] + [C] * i,
                            [C], attrs={"grudged": False,
                                        "grudge_memory": 0})

    def test_reset(self):
        """Check that grudged gets reset properly"""
        p1 = self.player()
        p2 = axelrod.Defector()
        p1.play(p2)
        p1.play(p2)
        p1.play(p2)
        self.assertTrue(p1.grudged)
        p1.reset()
        self.assertFalse(p1.grudged)
        self.assertEqual(p1.history, [])


class TestFoolMeOnce(TestPlayer):

    name = "Fool Me Once"
    player = axelrod.FoolMeOnce
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial(self):
        self.first_play_test(C)

    def test_strategy(self):
        """
        If opponent defects more than once, defect forever
        """
        self.responses_test([C], [D], [C])
        self.responses_test([C, C], [D, D], [D])
        self.responses_test([C, C], [D, C], [C])
        self.responses_test([C, C, C], [D, D, D], [D])


class TestForgetfulFoolMeOnce(TestPlayer):

    name = 'Forgetful Fool Me Once'
    player = axelrod.ForgetfulFoolMeOnce
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial(self):
        self.first_play_test(C)

    def test_strategy(self):
        """Test that will forgive one D but will grudge after 2 Ds, randomly
        forgets count"""
        random.seed(2)
        self.responses_test([C], [D], [C])
        self.responses_test([C, C], [D, D], [D])
        # Sometime eventually forget count:
        self.responses_test([C, C], [D, D], [D] * 13 + [C],
                            attrs={"D_count": 0})

    def test_reset(self):
        """Check that count gets reset properly"""
        P1 = self.player()
        P1.history = [C, D]
        P2 = axelrod.Player()
        P2.history = [D]
        random.seed(1)
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.D_count, 1)
        P1.reset()
        self.assertEqual(P1.D_count, 0)
        self.assertEqual(P1.history, [])


class TestFoolMeForever(TestPlayer):

    name = "Fool Me Forever"
    player = axelrod.FoolMeForever
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """
        If opponent defects more than once, defect forever
        """
        self.responses_test([], [], [D])
        self.responses_test([D], [D], [C])
        self.responses_test([D], [C], [D])
        self.responses_test([D, C], [D, C], [C])
        self.responses_test([D, C, C], [D, C, C], [C])
