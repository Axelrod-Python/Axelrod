"""Test for the grudger strategy."""

import random

import axelrod

from test_player import TestPlayer


class TestForgetfulGrudger(TestPlayer):

    name = "Forgetful Grudger"
    player = axelrod.ForgetfulGrudger
    stochastic = False

    def test_strategy(self):

        P1 = axelrod.ForgetfulGrudger()
        P2 = axelrod.Player()

        self.assertEqual(P1.grudged, False)

        # Starts by playing C
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('C')

        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('C')

        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('C')

        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('D')

        self.assertEqual(P2.history, ['C', 'C', 'C', 'D'])
        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.grudged, True)

        for turn in range(P1.mem_length-1):
            self.assertEqual(P1.strategy(P2), 'D')
            # Doesn't matter what opponent plays now
            P2.history.append(random.choice(['C', 'D']))
            self.assertEqual(P1.grudged, True)

        self.assertEqual(P1.strategy(P2), 'D')
        self.assertEqual(P1.grudge_memory, 10)
        self.assertEqual(P1.grudged, True)
        P2.history.append('C')

        # Back to being not grudged
        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('C')

        self.assertEqual(P1.strategy(P2), 'C')
        self.assertEqual(P1.grudged, False)
        P2.history.append('C')

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.ForgetfulGrudger()
        P1.history = ['C', 'D', 'D', 'D']
        P1.grudged = True
        P1.grudge_memory = 4
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.grudged, False)
        self.assertEqual(P1.grudge_memory, 0)
