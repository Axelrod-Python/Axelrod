"""Test for the once bitten strategy."""

import random

import axelrod

from test_player import TestPlayer


class TestOnceBitten(TestPlayer):

    name = "Once Bitten"
    player = axelrod.OnceBitten
    stochastic = False

    def test_initial_strategy(self):
        """Starts by cooperating."""
        P1 = axelrod.OnceBitten()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_strategy(self):
        """If opponent defects at any point then the player will defect forever."""
        P1 = axelrod.OnceBitten()
        P2 = axelrod.Player()
        # Starts by playing C
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('C')

        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('C')

        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('D')

        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('D')

        self.assertEqual(P2.history, ['C', 'C', 'D', 'D'])
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.grudged, True)

        for turn in range(P1.mem_length-1):
            self.assertEqual(P1.strategy(P2), 'D')
            # Doesn't matter what opponent plays now
            P2.history.append('C')
            self.assertEqual(P1.grudged, True)
            P2.history.append('D')
            self.assertEqual(P1.grudged, True)

        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.grudge_memory, 10)
        self.assertEqual(P1.grudged, True)
        P2.history.append('C')

    def test_reset(self):
        """Check that grudged gets reset properly"""
        P1 = self.player()
        P1.history = ['C', 'D']
        P2 = axelrod.Player()
        P2.history = ['D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertTrue(P1.grudged)
        P1.reset()
        self.assertFalse(P1.grudged)
        self.assertEqual(P1.history, [])

class TestFoolMeOnce(TestPlayer):

    name = "Fool Me Once"
    player = axelrod.FoolMeOnce
    stochastic = False

    def test_initial(self):
        P1 = axelrod.FoolMeOnce()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), P1._initial)

    def test_strategy(self):
        """
        If opponent defects at any point then the player will defect forever
        """
        P1 = axelrod.FoolMeOnce()
        P2 = axelrod.Defector()
        P1.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'D')


    def test_reset(self):
        """Check that count gets reset properly"""
        P1 = self.player()
        P1.history = ['C', 'D']
        P2 = axelrod.Player()
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.D_count, 1)
        P1.reset()
        self.assertEqual(P1.D_count, 0)
        self.assertEqual(P1.history, [])

class TestForgetfulFoolMeOnce(TestPlayer):

    name = 'Forgetful Fool Me Once'
    player = axelrod.ForgetfulFoolMeOnce
    stochastic = True

    def test_initial(self):
        P1 = axelrod.ForgetfulFoolMeOnce()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_strategy(self):
        """Test that will forgive one D but will grudge after 2 Ds, randomly forgets count"""
        random.seed(2)
        P1 = self.player()
        P2 = axelrod.Player()
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')
        P2.history = ['D', 'D']
        self.assertEqual(P1.strategy(P2), 'D')
        # Sometime will forget count:
        self.assertEqual(P1.strategy(P2), 'C')

    def test_reset(self):
        """Check that count gets reset properly"""
        P1 = self.player()
        P1.history = ['C', 'D']
        P2 = axelrod.Player()
        P2.history = ['D']
        random.seed(1)
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.D_count, 1)
        P1.reset()
        self.assertEqual(P1.D_count, 0)
        self.assertEqual(P1.history, [])

