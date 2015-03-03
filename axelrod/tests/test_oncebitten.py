"""Test for the once bitten strategy."""

import axelrod

from test_player import TestPlayer


class TestOnceBitten(TestPlayer):

    name = "Once Bitten"
    player = axelrod.OnceBitten

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
