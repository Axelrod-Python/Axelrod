"""Tests for Hidden Markov Model Strategies."""
import unittest

import axelrod
from .test_player import TestPlayer
from axelrod.strategies.hmm import SimpleHMM, is_stochastic_matrix

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestHMMPlayers(unittest.TestCase):
    """Test a few sample tables to make sure that the finite state machines are
    working as intended."""

    def test_is_stochastic_matrix(self):
        m = [[1, 0], [0, 1]]
        self.assertTrue(is_stochastic_matrix(m))
        m = [[1, 1e-20], [0, 1]]
        self.assertTrue(is_stochastic_matrix(m))
        m = [[0.6, 0.4], [0.8, 0.2]]
        self.assertTrue(is_stochastic_matrix(m))
        m = [[0.6, 0.6], [0.8, 0.2]]
        self.assertFalse(is_stochastic_matrix(m))
        m = [[0.6, 0.4], [0.8, 1.2]]
        self.assertFalse(is_stochastic_matrix(m))

    def test_cooperator(self):
        """Tests that the player defined by the table for Cooperator is in fact
        Cooperator."""
        t_C = [[1]]
        t_D = [[1]]
        p = [1]
        player = axelrod.HMMPlayer(t_C, t_D, p, initial_state=0, initial_action=C)
        self.assertFalse(player.is_stochastic())
        self.assertFalse(player.classifier['stochastic'])
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C] * 6)

    def test_defector(self):
        """Tests that the player defined by the table for Defector is in fact
        Defector."""
        t_C = [[1]]
        t_D = [[1]]
        p = [0]
        player = axelrod.HMMPlayer(t_C, t_D, p, initial_state=0, initial_action=D)
        self.assertFalse(player.is_stochastic())
        self.assertFalse(player.classifier['stochastic'])
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [D] * 6)

    def test_tft(self):
        """Tests that the player defined by the table for TFT is in fact
        TFT."""
        t_C = [[1, 0], [1, 0]]
        t_D = [[0, 1], [0, 1]]
        p = [1, 0]
        player = axelrod.HMMPlayer(t_C, t_D, p, initial_state=0, initial_action=C)
        self.assertFalse(player.is_stochastic())
        self.assertFalse(player.classifier['stochastic'])
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C, C, D, C, D, C])

    def test_wsls(self):
        """Tests that the player defined by the table for TFT is in fact
        WSLS (also known as Pavlov."""
        t_C = [[1, 0], [0, 1]]
        t_D = [[0, 1], [1, 0]]
        p = [1, 0]
        player = axelrod.HMMPlayer(t_C, t_D, p, initial_state=0, initial_action=C)
        self.assertFalse(player.is_stochastic())
        self.assertFalse(player.classifier['stochastic'])
        opponent = axelrod.Alternator()
        for i in range(6):
            player.play(opponent)
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C, C, D, D, C, C])

    def test_malformed_params(self):
        # Test a malformed table
        t_C = [[1, 0.5], [0, 1]]
        self.assertFalse(is_stochastic_matrix(t_C))

        t_C = [[1, 0], [0, 1]]
        t_D = [[0, 1], [1, 0]]
        p = [1, 0]
        hmm = SimpleHMM(t_C, t_C, p, 0)
        self.assertTrue(hmm.is_well_formed())
        hmm = SimpleHMM(t_C, t_D, p, -1)
        self.assertFalse(hmm.is_well_formed())
        t_C = [[1, -1], [0, 1]]
        t_D = [[0, 1], [1, 0]]
        p = [1, 0]
        hmm = SimpleHMM(t_C, t_D, p, 0)
        self.assertFalse(hmm.is_well_formed())
        t_C = [[1, 0], [0, 1]]
        t_D = [[0, 2], [1, 0]]
        p = [1, 0]
        hmm = SimpleHMM(t_C, t_D, p, 0)
        self.assertFalse(hmm.is_well_formed())
        t_C = [[1, 0], [0, 1]]
        t_D = [[0, 1], [1, 0]]
        p = [-1, 2]
        hmm = SimpleHMM(t_C, t_D, p, 0)
        self.assertFalse(hmm.is_well_formed())


class TestHMMPlayer(TestPlayer):

    name = "HMM Player"
    player = axelrod.HMMPlayer

    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_reset(self):
        player = self.player([[1]], [[1]], [0], initial_state=0)
        player.hmm.state = -1
        player.reset()
        self.assertFalse(player.hmm.state == -1)
