"""Tests for Hidden Markov Model Strategies."""

import unittest

import axelrod as axl
from axelrod.evolvable_player import InsufficientParametersError
from axelrod.strategies.hmm import (
    EvolvableHMMPlayer,
    HMMPlayer,
    SimpleHMM,
    is_stochastic_matrix,
)

from .test_evolvable_player import PartialClass, TestEvolvablePlayer
from .test_player import TestMatch, TestPlayer

C, D = axl.Action.C, axl.Action.D


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
        player = axl.HMMPlayer(
            transitions_C=t_C,
            transitions_D=t_D,
            emission_probabilities=p,
            initial_state=0,
            initial_action=C,
        )
        self.assertFalse(player.is_stochastic())
        self.assertFalse(axl.Classifiers["stochastic"](player))
        opponent = axl.Alternator()
        match = axl.Match((player, opponent), turns=6)
        match.play()
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C] * 6)

    def test_defector(self):
        """Tests that the player defined by the table for Defector is in fact
        Defector."""
        t_C = [[1]]
        t_D = [[1]]
        p = [0]
        player = axl.HMMPlayer(
            transitions_C=t_C,
            transitions_D=t_D,
            emission_probabilities=p,
            initial_state=0,
            initial_action=D,
        )
        self.assertFalse(player.is_stochastic())
        self.assertFalse(axl.Classifiers["stochastic"](player))
        opponent = axl.Alternator()
        match = axl.Match((player, opponent), turns=6)
        match.play()
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [D] * 6)

    def test_tft(self):
        """Tests that the player defined by the table for TFT is in fact
        TFT."""
        t_C = [[1, 0], [1, 0]]
        t_D = [[0, 1], [0, 1]]
        p = [1, 0]
        player = axl.HMMPlayer(
            transitions_C=t_C,
            transitions_D=t_D,
            emission_probabilities=p,
            initial_state=0,
            initial_action=C,
        )
        self.assertFalse(player.is_stochastic())
        self.assertFalse(axl.Classifiers["stochastic"](player))
        opponent = axl.Alternator()
        match = axl.Match((player, opponent), turns=6)
        match.play()
        self.assertEqual(opponent.history, [C, D] * 3)
        self.assertEqual(player.history, [C, C, D, C, D, C])

    def test_wsls(self):
        """Tests that the player defined by the table for WSLS is in fact
        WSLS (also known as Pavlov)."""
        t_C = [[1, 0], [0, 1]]
        t_D = [[0, 1], [1, 0]]
        p = [1, 0]
        player = axl.HMMPlayer(
            transitions_C=t_C,
            transitions_D=t_D,
            emission_probabilities=p,
            initial_state=0,
            initial_action=C,
        )
        self.assertFalse(player.is_stochastic())
        self.assertFalse(axl.Classifiers["stochastic"](player))
        opponent = axl.Alternator()
        match = axl.Match((player, opponent), turns=6)
        match.play()
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

    name = "HMM Player: 0, C"
    player = axl.HMMPlayer

    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_reset(self):
        player = self.player(
            transitions_C=[[1]],
            transitions_D=[[1]],
            emission_probabilities=[0],
            initial_state=0,
        )
        player.hmm.state = -1
        player.reset()
        self.assertFalse(player.hmm.state == -1)


class TestEvolvedHMM5(TestPlayer):

    name = "Evolved HMM 5"
    player = axl.EvolvedHMM5

    expected_classifier = {
        "memory_depth": 5,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(
            opponent=axl.Alternator(), expected_actions=actions, seed=2
        )


class TestEvolvedHMM5vsCooperator(TestMatch):
    def test_rounds(self):
        self.versus_test(
            axl.EvolvedHMM5(), axl.Cooperator(), [C] * 5, [C] * 5, seed=3
        )


class TestEvolvedHMM5vsDefector(TestMatch):
    def test_rounds(self):
        self.versus_test(
            axl.EvolvedHMM5(), axl.Defector(), [C, C, D], [D, D, D], seed=5
        )


class TestEvolvableHMMPlayer(unittest.TestCase):

    player_class = EvolvableHMMPlayer

    def test_normalized_parameters(self):
        transitions_C = [[1, 0], [1, 0]]
        transitions_D = [[0, 1], [0, 1]]
        emission_probabilities = [1, 0]
        initial_state = 0
        initial_action = C

        self.assertRaises(
            InsufficientParametersError, self.player_class, seed=1
        )
        self.assertRaises(
            InsufficientParametersError,
            self.player_class,
            transitions_C=transitions_C,
            transitions_D=transitions_D,
            emission_probabilities=emission_probabilities,
            initial_state=None,
            seed=1,
        )
        self.assertRaises(
            InsufficientParametersError,
            self.player_class,
            transitions_C=transitions_C,
            transitions_D=transitions_D,
            emission_probabilities=emission_probabilities,
            initial_action=None,
            seed=1,
        )
        self.assertRaises(
            InsufficientParametersError,
            self.player_class,
            initial_state=initial_state,
            initial_action=initial_action,
            seed=1,
        )

    def test_vector_to_instance(self):
        num_states = 4
        vector = []
        rng = axl.RandomGenerator(seed=1111)
        for _ in range(2 * num_states):
            vector.extend(list(rng.random_vector(num_states)))
        for _ in range(num_states + 1):
            vector.append(rng.random())
        player = self.player_class(num_states=num_states, seed=1)
        player.receive_vector(vector=vector)
        self.assertIsInstance(player, self.player_class)

    def test_create_vector_bounds(self):
        num_states = 4
        size = 2 * num_states**2 + num_states + 1

        player = self.player_class(num_states=num_states, seed=1)
        lb, ub = player.create_vector_bounds()

        self.assertIsInstance(lb, list)
        self.assertEqual(len(lb), size)
        self.assertIsInstance(ub, list)
        self.assertEqual(len(ub), size)


class TestEvolvableHMMPlayer2(TestEvolvablePlayer):
    name = "EvolvableHMMPlayer"
    player_class = EvolvableHMMPlayer
    parent_class = HMMPlayer
    parent_kwargs = [
        "transitions_C",
        "transitions_D",
        "emission_probabilities",
        "initial_state",
        "initial_action",
    ]
    init_parameters = {"num_states": 4}


class TestEvolvableHMMPlayer3(TestEvolvablePlayer):
    name = "EvolvableHMMPlayer"
    player_class = EvolvableHMMPlayer
    parent_class = HMMPlayer
    parent_kwargs = [
        "transitions_C",
        "transitions_D",
        "emission_probabilities",
        "initial_state",
        "initial_action",
    ]
    init_parameters = {"num_states": 8}


class TestEvolvableHMMPlayer4(TestEvolvablePlayer):
    name = "EvolvableHMMPlayer"
    player_class = EvolvableHMMPlayer
    parent_class = HMMPlayer
    parent_kwargs = [
        "transitions_C",
        "transitions_D",
        "emission_probabilities",
        "initial_state",
        "initial_action",
    ]
    init_parameters = {
        "transitions_C": [[1, 0], [1, 0]],
        "transitions_D": [[0, 1], [0, 1]],
        "emission_probabilities": [1, 0],
        "initial_state": 0,
        "initial_action": C,
    }


# Substitute EvolvableHMMPlayer as a regular HMMPlayer.
EvolvableHMMPlayerWithDefault = PartialClass(
    EvolvableHMMPlayer,
    transitions_C=[[1]],
    transitions_D=[[1]],
    emission_probabilities=[0.5],
    initial_state=0,
)


class EvolvableHMMPlayerAsHMMPlayer(TestHMMPlayer):
    player = EvolvableHMMPlayerWithDefault

    def test_equality_of_clone(self):
        pass

    def test_equality_of_pickle_clone(self):
        pass

    def test_repr(self):
        pass
