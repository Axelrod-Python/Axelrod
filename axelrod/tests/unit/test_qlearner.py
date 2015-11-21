"""Test for the qlearner strategy."""

import random

import axelrod
from axelrod import simulate_play, Game

from .test_player import TestPlayer, test_responses

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestRiskyQLearner(TestPlayer):

    name = 'Risky QLearner'
    player = axelrod.RiskyQLearner
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_payoff_matrix(self):
        (R, P, S, T) = Game().RPST()
        payoff_matrix = {C: {C: R, D: S}, D: {C: T, D: P}}
        p1 = self.player()
        self.assertEqual(p1.payoff_matrix, payoff_matrix)

    def test_qs_update(self):
        """Test that the q and v values update."""
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.Qs, {'': {C: 0, D: 0.9}, '0.0': {C: 0, D: 0}})
        simulate_play(p1, p2)
        self.assertEqual(p1.Qs,{'': {C: 0, D: 0.9}, '0.0': {C: 2.7, D: 0}, 'C1.0': {C: 0, D: 0}})

    def test_vs_update(self):
        """Test that the q and v values update."""
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs, {'': 0.9, '0.0': 0})
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs,{'': 0.9, '0.0': 2.7, 'C1.0': 0})

    def test_prev_state_updates(self):
        """Test that the q and v values update."""
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, '0.0')
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_strategy(self):
        """Tests that it chooses the best strategy."""
        random.seed(5)
        p1 = axelrod.RiskyQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {C: 0, D: 0}, 'CCDC': {C: 2, D: 6}}
        p2 = axelrod.Cooperator()
        test_responses(self, p1, p2, [], [], [C, D, C, C, D, C, C])

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.RiskyQLearner()
        P1.Qs = {'': {C: 0, D: -0.9}, '0.0': {C: 0, D: 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = [C, D, D, D]
        P1.prev_state = C
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'': 0})
        self.assertEqual(P1.Qs, {'': {C: 0, D: 0}})


class TestArrogantQLearner(TestPlayer):

    name = 'Arrogant QLearner'
    player = axelrod.ArrogantQLearner
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_qs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.ArrogantQLearner()
        p2 = axelrod.Cooperator()
        play_1, play_2 = simulate_play(p1, p2)
        self.assertEqual(p1.Qs, {'': {C: 0, D: 0.9}, '0.0': {C: 0, D: 0}})
        simulate_play(p1, p2)
        self.assertEqual(p1.Qs,{'': {C: 0, D: 0.9}, '0.0': {C: 2.7, D: 0}, 'C1.0': {C: 0, D: 0}})

    def test_vs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.ArrogantQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs, {'': 0.9, '0.0': 0})
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs,{'': 0.9, '0.0': 2.7, 'C1.0': 0})

    def test_prev_state_updates(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.ArrogantQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, '0.0')
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_strategy(self):
        """Tests that it chooses the best strategy."""
        random.seed(9)
        p1 = axelrod.ArrogantQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {C: 0, D: 0}, 'CCDC': {C: 2, D: 6}}
        p2 = axelrod.Cooperator()
        test_responses(self, p1, p2, [], [], [C, C, C, C, C, C, C])

    def test_reset_method(self):
        """Tests the reset method."""
        P1 = axelrod.ArrogantQLearner()
        P1.Qs = {'': {C: 0, D: -0.9}, '0.0': {C: 0, D: 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = [C, D, D, D]
        P1.prev_state = C
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'':0})
        self.assertEqual(P1.Qs, {'':{C:0, D:0}})


class TestHesitantQLearner(TestPlayer):

    name = 'Hesitant QLearner'
    player = axelrod.HesitantQLearner
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_qs_update(self):
        """Test that the q and v values update."""
        random.seed(5)
        p1 = axelrod.HesitantQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.Qs, {'': {C: 0, D: 0.1}, '0.0': {C: 0, D: 0}})
        simulate_play(p1, p2)
        self.assertEqual(p1.Qs,{'': {C: 0, D: 0.1}, '0.0': {C: 0.30000000000000004, D: 0}, 'C1.0': {C: 0, D: 0}})

    def test_vs_update(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.HesitantQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs, {'': 0.1, '0.0': 0})
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs,{'': 0.1, '0.0': 0.30000000000000004, 'C1.0': 0})

    def test_prev_state_updates(self):
        """
        Test that the q and v values update
        """
        random.seed(5)
        p1 = axelrod.HesitantQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, '0.0')
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_strategy(self):
        """Tests that it chooses the best strategy."""
        random.seed(9)
        p1 = axelrod.HesitantQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {C: 0, D: 0}, 'CCDC': {C: 2, D: 6}}
        p2 = axelrod.Cooperator()
        test_responses(self, p1, p2, [], [], [C, C, C, C, C, C, C])

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.HesitantQLearner()
        P1.Qs = {'': {C: 0, D: -0.9}, '0.0': {C: 0, D: 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = [C, D, D, D]
        P1.prev_state = C
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'': 0})
        self.assertEqual(P1.Qs, {'': {C: 0, D: 0}})


class TestCautiousQLearner(TestPlayer):

    name = 'Cautious QLearner'
    player = axelrod.CautiousQLearner
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_qs_update(self):
        """Test that the q and v values update."""
        random.seed(5)
        p1 = axelrod.CautiousQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.Qs, {'': {C: 0, D: 0.1}, '0.0': {C: 0, D: 0}})
        simulate_play(p1, p2)
        self.assertEqual(p1.Qs,{'': {C: 0, D: 0.1}, '0.0': {C: 0.30000000000000004, D: 0}, 'C1.0': {C: 0, D: 0.0}})

    def test_vs_update(self):
        """Test that the q and v values update."""
        random.seed(5)
        p1 = axelrod.CautiousQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs, {'': 0.1, '0.0': 0})
        simulate_play(p1, p2)
        self.assertEqual(p1.Vs,{'': 0.1, '0.0': 0.30000000000000004, 'C1.0': 0})

    def test_prev_state_updates(self):
        """Test that the q and v values update."""
        random.seed(5)
        p1 = axelrod.CautiousQLearner()
        p2 = axelrod.Cooperator()
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, '0.0')
        simulate_play(p1, p2)
        self.assertEqual(p1.prev_state, 'C1.0')

    def test_strategy(self):
        """Tests that it chooses the best strategy."""
        random.seed(9)
        p1 = axelrod.CautiousQLearner()
        p1.state = 'CCDC'
        p1.Qs = {'': {C: 0, D: 0}, 'CCDC': {C: 2, D: 6}}
        p2 = axelrod.Cooperator()
        test_responses(self, p1, p2, [], [], [C, C, C, C, C, C, C])

    def test_reset_method(self):
        """Tests the reset method."""
        P1 = axelrod.CautiousQLearner()
        P1.Qs = {'': {C: 0, D: -0.9}, '0.0': {C: 0, D: 0}}
        P1.Vs = {'': 0, '0.0': 0}
        P1.history = [C, D, D, D]
        P1.prev_state = C
        P1.reset()
        self.assertEqual(P1.prev_state, '')
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.Vs, {'': 0})
        self.assertEqual(P1.Qs, {'': {C: 0, D: 0}})
