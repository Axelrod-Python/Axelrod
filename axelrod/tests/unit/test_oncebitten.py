"""Test for the once bitten strategy."""

import random

import axelrod

from .test_player import TestPlayer

C, D = 'C', 'D'


class TestOnceBitten(TestPlayer):

    name = "Once Bitten"
    player = axelrod.OnceBitten
    expected_classifier = {
        'memory_depth': 12,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.OnceBitten()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), C)

    def test_strategy(self):
        """If opponent defects at any point then the player will defect
        forever."""
        P1 = axelrod.OnceBitten()
        P2 = axelrod.Player()
        # Starts by playing C
        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        P2.history.append(C)

        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        P2.history.append(C)

        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        P2.history.append(D)

        self.assertEqual(P1.strategy(P2), C)
        self.assertEqual(P1.grudged, False)
        P2.history.append(D)

        self.assertEqual(P2.history, [C, C, D, D])
        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudged, True)

        for turn in range(P1.mem_length-1):
            self.assertEqual(P1.strategy(P2), D)
            # Doesn't matter what opponent plays now
            P2.history.append(C)
            self.assertEqual(P1.grudged, True)
            P2.history.append(D)
            self.assertEqual(P1.grudged, True)

        self.assertEqual(P1.strategy(P2), D)
        self.assertEqual(P1.grudge_memory, 10)
        self.assertEqual(P1.grudged, True)
        P2.history.append(C)

    def test_reset(self):
        """Check that grudged gets reset properly"""
        P1 = self.player()
        P1.history = [C, D]
        P2 = axelrod.Player()
        P2.history = [D, D]
        self.assertEqual(P1.strategy(P2), D)
        self.assertTrue(P1.grudged)
        P1.reset()
        self.assertFalse(P1.grudged)
        self.assertEqual(P1.history, [])


class TestFoolMeOnce(TestPlayer):

    name = "Fool Me Once"
    player = axelrod.FoolMeOnce
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
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
        self.responses_test([C, C], [D, D], [D] * 13 + [C])

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
