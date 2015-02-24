"""
Test for the qlearner strategy
"""
import unittest
import axelrod
import random

class TestRiskyQLearner(unittest.TestCase):

    def test_qs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs, {'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0, 'D': 0}})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs,{'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0.9, 'D': 0}, 'C1.0': {'C': 0, 'D': 0}})

    def test_vs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs, {'': 0, '0.0': 0})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs,{'': 0, '0.0': 0.9, 'C1.0': 0})

    def test_prev_state_updates(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, '0.0')
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_choose_best_strategy(self):
        """
        Tests that it chooses the best strategy
        """
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {'C': 0, 'D': 0}, 'CCDC': {'C': 2, 'D': 6}}
        p2 = axelrod.Cooperator()
        self.assertEqual(p1.strategy(p2), 'C')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.RiskyQLearner()
        P1.Qs = {'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0, 'D': 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = ['C', 'D', 'D', 'D']
        P1.prev_state = 'C'
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'':0})
        self.assertEqual(P1.Qs, {'':{'C':0, 'D':0}})

    def test_representation(self):
        """
        Tests string representation of class
        """
        P1 = axelrod.RiskyQLearner()
        self.assertEqual(str(P1), 'Risky QLearner')

    def test_stochastic(self):
        self.assertTrue(axelrod.RiskyQLearner().stochastic)

class TestArrogantQLearner(unittest.TestCase):

    def test_qs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.ArrogantQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs, {'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0, 'D': 0}})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs,{'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0.9, 'D': 0}, 'C1.0': {'C': 0, 'D': 0}})

    def test_vs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.ArrogantQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs, {'': 0, '0.0': 0})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs,{'': 0, '0.0': 0.9, 'C1.0': 0})

    def test_prev_state_updates(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.ArrogantQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, '0.0')
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_choose_best_strategy(self):
        """
        Tests that it chooses the best strategy
        """
        random.seed(9)
        p1 = axelrod.ArrogantQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {'C': 0, 'D': 0}, 'CCDC': {'C': 2, 'D': 6}}
        p2 = axelrod.Cooperator()
        self.assertEqual(p1.strategy(p2), 'C')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.ArrogantQLearner()
        P1.Qs = {'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0, 'D': 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = ['C', 'D', 'D', 'D']
        P1.prev_state = 'C'
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'':0})
        self.assertEqual(P1.Qs, {'':{'C':0, 'D':0}})

    def test_representation(self):
        """
        Tests string representation of class
        """
        P1 = axelrod.ArrogantQLearner()
        self.assertEqual(str(P1), 'Arrogant QLearner')

    def test_stochastic(self):
        self.assertTrue(axelrod.ArrogantQLearner().stochastic)


class TestHesitantQLearner(unittest.TestCase):

    def test_qs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.HesitantQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs, {'': {'C': 0, 'D': -0.1}, '0.0': {'C': 0, 'D': 0}})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs,{'': {'C': 0, 'D': -0.1}, '0.0': {'C': 0.1, 'D': 0}, 'C1.0': {'C': 0, 'D': 0}})

    def test_vs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.HesitantQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs, {'': 0, '0.0': 0})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs,{'': 0, '0.0': 0.1, 'C1.0': 0})

    def test_prev_state_updates(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.HesitantQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, '0.0')
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_choose_best_strategy(self):
        """
        Tests that it chooses the best strategy
        """
        random.seed(9)
        p1 = axelrod.HesitantQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {'C': 0, 'D': 0}, 'CCDC': {'C': 2, 'D': 6}}
        p2 = axelrod.Cooperator()
        self.assertEqual(p1.strategy(p2), 'C')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.HesitantQLearner()
        P1.Qs = {'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0, 'D': 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = ['C', 'D', 'D', 'D']
        P1.prev_state = 'C'
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'':0})
        self.assertEqual(P1.Qs, {'':{'C':0, 'D':0}})

    def test_representation(self):
        """
        Tests string representation of class
        """
        P1 = axelrod.HesitantQLearner()
        self.assertEqual(str(P1), 'Hesitant QLearner')

    def test_stochastic(self):
        self.assertTrue(axelrod.HesitantQLearner().stochastic)


class TestCautiousQLearner(unittest.TestCase):

    def test_qs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.CautiousQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs, {'': {'C': 0, 'D': -0.1}, '0.0': {'C': 0, 'D': 0}})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Qs,{'': {'C': 0, 'D': -0.1}, '0.0': {'C': 0.1, 'D': 0}, 'C1.0': {'C': 0, 'D': 0}})

    def test_vs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.CautiousQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs, {'': 0, '0.0': 0})
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.Vs,{'': 0, '0.0': 0.1, 'C1.0': 0})

    def test_prev_state_updates(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.CautiousQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, '0.0')
        play_1, play_2 = p1.strategy(p2), p2.strategy(p1)
        p1.history.append(play_1)
        p2.history.append(play_2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_choose_best_strategy(self):
        """
        Tests that it chooses the best strategy
        """
        random.seed(9)
        p1 = axelrod.CautiousQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {'C': 0, 'D': 0}, 'CCDC': {'C': 2, 'D': 6}}
        p2 = axelrod.Cooperator()
        self.assertEqual(p1.strategy(p2), 'C')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')
        self.assertEqual(p1.strategy(p2), 'D')

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.CautiousQLearner()
        P1.Qs = {'': {'C': 0, 'D': -0.9}, '0.0': {'C': 0, 'D': 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = ['C', 'D', 'D', 'D']
        P1.prev_state = 'C'
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'':0})
        self.assertEqual(P1.Qs, {'':{'C':0, 'D':0}})

    def test_representation(self):
        """
        Tests string representation of class
        """
        P1 = axelrod.CautiousQLearner()
        self.assertEqual(str(P1), 'Cautious QLearner')

    def test_stochastic(self):
        self.assertTrue(axelrod.CautiousQLearner().stochastic)
