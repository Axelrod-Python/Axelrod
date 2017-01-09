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
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """If opponent defects at any point then the player will defect
        forever."""
        # Become grudged if the opponent defects twice in a row
        self.responses_test(C, attrs={"grudged": False})
        self.responses_test(C, C, C, attrs={"grudged": False})
        self.responses_test(C, C + C, C + C, attrs={"grudged": False})
        self.responses_test(C, C * 3, C + C + D, attrs={"grudged": False})
        self.responses_test(D, C * 4, C + C + D + D, attrs={"grudged": True})

        mem_length = self.player().mem_length
        for i in range(mem_length - 1):
            self.responses_test(D, C * 4 + D * i, C + C + D + D + D * i,
                                attrs={"grudged": True,
                                       "grudge_memory": i})
        i = mem_length + 1
        self.responses_test(C, C * 4 + D * i, C + C + D + D + C * i,
                            attrs={"grudged": False,
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


class TestFoolMeOnce(TestPlayer):

    name = "Fool Me Once"
    player = axelrod.FoolMeOnce
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
        # Start by cooperating.
        self.first_play_test(C)
        # If opponent defects more than once, defect forever.
        self.responses_test(C, C, D)
        self.responses_test(D, C + C, D + D)
        self.responses_test(C, C + C, D + C)
        self.responses_test(D, C * 3, D * 3)


class TestForgetfulFoolMeOnce(TestPlayer):

    name = 'Forgetful Fool Me Once'
    player = axelrod.ForgetfulFoolMeOnce
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C)
        # Test that will forgive one D but will grudge after 2 Ds, randomly
        # forgets count
        random.seed(2)
        self.responses_test(C, C, D)
        self.responses_test(D, C + C, D + D)
        # Sometime eventually forget count:
        self.responses_test(D * 18 + C, C + C, D + D,
                            attrs={"D_count": 0}, random_seed=2)

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
        self.assertEqual(len(P1.history), 0)


class TestFoolMeForever(TestPlayer):

    name = "Fool Me Forever"
    player = axelrod.FoolMeForever
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
        # If opponent defects more than once, defect forever.
        self.responses_test(D)
        self.responses_test(C, D, D)
        self.responses_test(D, D, C)
        self.responses_test(C, D + C, D + C)
        self.responses_test(C, D + C + C, D + C + C)
