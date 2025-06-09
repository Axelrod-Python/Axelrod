"""Tests for the Attention strategies."""

import unittest
from unittest.mock import patch

import torch

import axelrod as axl
from axelrod.load_data_ import load_attention_model_weights
from axelrod.strategies.attention import (
    MEMORY_LENGTH,
    GameState,
    PlayerModel,
    actions_to_game_state,
    compute_features,
)

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestFeatureComputation(unittest.TestCase):
    """Test the feature computation functionality."""

    def test_compute_features(self):
        """Test that features are computed correctly."""
        player = axl.MockPlayer(actions=[C, D, C, D])
        opponent = axl.MockPlayer(actions=[D, C, C, D])
        # Play the actions to populate history
        match = axl.Match((player, opponent), turns=4)
        match.play()

        features = compute_features(player, opponent)

        # Check the shape and type
        self.assertIsInstance(features, torch.Tensor)
        self.assertEqual(features.shape, (len(player.history) + 1,))

        # Check specific values (CLS token and game states)
        self.assertEqual(features[0].item(), 0)  # CLS token
        self.assertEqual(features[1].item(), GameState.DefectDefect)
        self.assertEqual(features[2].item(), GameState.CooperateCooperate)
        self.assertEqual(features[3].item(), GameState.DefectCooperate)
        self.assertEqual(features[4].item(), GameState.CooperateDefect)

    def test_compute_features_right_pad(self):
        """Test that features are computed correctly."""
        player = axl.MockPlayer(actions=[C, D, C, D])
        opponent = axl.MockPlayer(actions=[D, C, C, D])
        # Play the actions to populate history
        match = axl.Match((player, opponent), turns=4)
        match.play()

        features = compute_features(player, opponent, True)

        # Check the shape and type
        self.assertIsInstance(features, torch.Tensor)
        self.assertEqual(features.shape, (MEMORY_LENGTH + 1,))

        # Check specific values (CLS token and game states)
        self.assertEqual(features[0].item(), 0)  # CLS token
        self.assertEqual(features[1].item(), GameState.DefectDefect)
        self.assertEqual(features[2].item(), GameState.CooperateCooperate)
        self.assertEqual(features[3].item(), GameState.DefectCooperate)
        self.assertEqual(features[4].item(), GameState.CooperateDefect)

    def test_actions_to_game_state(self):
        """Test the mapping from actions to game states."""
        self.assertEqual(
            actions_to_game_state(C, C), GameState.CooperateCooperate
        )
        self.assertEqual(actions_to_game_state(C, D), GameState.CooperateDefect)
        self.assertEqual(actions_to_game_state(D, C), GameState.DefectCooperate)
        self.assertEqual(actions_to_game_state(D, D), GameState.DefectDefect)


class TestEvolvedAttention(TestPlayer):
    name = "EvolvedAttention"
    player = axl.EvolvedAttention
    expected_classifier = {
        "memory_depth": MEMORY_LENGTH,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": True,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_model_initialization(self):
        """Test that the model is initialized correctly."""
        player = self.player()
        self.assertIsNone(player.model)

    def test_load_model(self):
        """Test that the model can be loaded correctly."""
        with patch(
            "axelrod.strategies.attention.load_attention_model_weights",
            wraps=load_attention_model_weights,
        ) as load_attention_model_weights_spy:
            player = self.player()
            self.assertIsNone(player.model)
            player.load_model()
            self.assertIsInstance(player.model, PlayerModel)
            player.load_model()
            self.assertIsInstance(player.model, PlayerModel)
            load_attention_model_weights_spy.assert_called_once()

    def test_versus_cooperator(self):
        actions = [(C, C)] * 5
        self.versus_test(axl.Cooperator(), expected_actions=actions)

    def test_versus_defector(self):
        actions = [(C, D), (C, D)] + [(D, D)] * 3
        self.versus_test(axl.Defector(), expected_actions=actions)

    def test_versus_alternator(self):
        actions = [(C, C), (C, D), (C, C), (D, D), (D, C), (D, D)]
        self.versus_test(axl.Alternator(), expected_actions=actions)

    def test_versus_handshake(self):
        actions = [(C, C), (C, D), (C, D), (D, D), (D, D), (C, D)]
        self.versus_test(axl.Handshake(), expected_actions=actions)
