"""Tests for the Attention strategies."""

import unittest

import torch

import axelrod as axl
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
        self.assertIsInstance(player.model, PlayerModel)

    def test_versus_cooperator(self):
        actions = [(C, C)] * 5
        self.versus_test(axl.Cooperator(), expected_actions=actions)
