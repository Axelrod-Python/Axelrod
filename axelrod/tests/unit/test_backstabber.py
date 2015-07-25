import axelrod

from test_player import TestPlayer


class TestBackStabber(TestPlayer):

    name = "BackStabber"
    player = axelrod.BackStabber
    stochastic = False

    def test_initial(self):
        P1 = axelrod.BackStabber()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), P1._initial)

    def test_strategy(self):
        """
        Forgives the first 3 defections but on the fourth
        will defect forever. Defects after the 198th round unconditionally.
        """
        P1 = axelrod.BackStabber()
        P2 = axelrod.Defector()
        P1.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P1.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P1.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P1.history.append('D')
        self.assertEqual(P1.strategy(P2), 'D')
        P2.history = ['C'] * 197
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


class DoubleCrosser(TestPlayer):

    name = "DoubleCrosser"
    player = axelrod.DoubleCrosser
    stochastic = False

    def test_initial(self):
        P1 = axelrod.DoubleCrosser()
        P2 = axelrod.Player()
        self.assertEqual(P1.strategy(P2), P1._initial)

    def test_strategy(self):
        """
        Forgives the first 3 defections but on the fourth
        will defect forever. If the opponent did not defect
        in the first 6 rounds the player will cooperate until
        the 180th round. Defects after the 198th round unconditionally.
        """
        P1 = axelrod.BackStabber()
        P2 = axelrod.Defector()
        P2.history = ['C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'C']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history = ['C']
        P2.history = ['D']
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'C')
        P1.history.append('C')
        P2.history.append('D')
        self.assertEqual(P1.strategy(P2), 'D')
        P2.history = ['C'] * 197
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
