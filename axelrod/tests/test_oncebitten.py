"""
Test for the once bitten strategy
"""
import unittest
import axelrod

class TestOnceBitten(unittest.TestCase):

    def test_initial_strategy(self):
        """
        Starts by cooperating
        """
        P1 = axelrod.OnceBitten()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), 'C')

    def test_effect_of_strategy(self):
        """
        If opponent defects at any point then the player will defect forever
        """
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

    def test_representation(self):
        P1 = axelrod.OnceBitten()
        self.assertEqual(str(P1), 'Once Bitten')

    def test_stochastic(self):
        self.assertFalse(axelrod.OnceBitten().stochastic)

class TestFoolMeOnce(unittest.TestCase):

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

    def test_representation(self):
        P1 = axelrod.FoolMeOnce()
        self.assertEqual(str(P1), 'Fool Me Once')

    def test_stochastic(self):
        self.assertFalse(axelrod.FoolMeOnce().stochastic)

class TestForgetfulFoolMeOnce(unittest.TestCase):

    def test_initial(self):
        P1 = axelrod.ForgetfulFoolMeOnce()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), P1._initial)

    def test_representation(self):
        P1 = axelrod.ForgetfulFoolMeOnce()
        self.assertEqual(str(P1), 'Forgetful Fool Me Once')

    def test_stochastic(self):
        self.assertTrue(axelrod.ForgetfulFoolMeOnce().stochastic)

