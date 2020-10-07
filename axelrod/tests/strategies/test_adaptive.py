"""Tests for the Adaptive strategy."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestAdaptive(TestPlayer):

    name = "Adaptive"
    player = axl.Adaptive
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": {"game"},
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_default_initial_actions_against_cooperator(self):
        coplayer = axl.Cooperator()
        player_actions = [C] * 6 + [D] * 8
        coplayer_actions = [C] * 14
        expected_actions = list(zip(player_actions, coplayer_actions))
        self.versus_test(coplayer, expected_actions=expected_actions)

    def test_default_initial_actions_against_defector(self):
        coplayer = axl.Defector()
        player_actions = [C] * 6 + [D] * 8
        coplayer_actions = [D] * 14
        expected_actions = list(zip(player_actions, coplayer_actions))
        self.versus_test(coplayer, expected_actions=expected_actions)

    def test_default_initial_actions_against_alternator(self):
        coplayer = axl.Alternator()
        player_actions = [C] * 6 + [D] * 8
        coplayer_actions = [C, D] * 7
        expected_actions = list(zip(player_actions, coplayer_actions))
        self.versus_test(coplayer, expected_actions=expected_actions)

    def test_default_initial_actions_against_tft(self):
        coplayer = axl.TitForTat()
        player_actions = [C] * 6 + [D] * 5 + [C, C]
        coplayer_actions = [C] * 7 + [D] * 5 + [C]
        expected_actions = list(zip(player_actions, coplayer_actions))
        self.versus_test(coplayer, expected_actions=expected_actions)

    def test_scoring_with_default_game(self):
        """Tests that the default game is used in scoring."""
        opponent = axl.Cooperator()
        attrs = {"scores": {C: 3, D: 0}}
        expected_actions = list(zip([C, C], [C, C]))
        self.versus_test(
            opponent, expected_actions, turns=2, attrs=attrs, seed=9
        )

    def test_scoring_with_alternate_game(self):
        """Tests that the alternate game is used in scoring."""
        opponent = axl.Alternator()
        expected_actions = list(zip([C, C, C], [C, D, C]))
        attrs = {"scores": {C: 7, D: 0}}
        match_attributes = {"game": axl.Game(-3, 10, 10, 10)}
        self.versus_test(
            opponent,
            expected_actions,
            turns=3,
            attrs=attrs,
            seed=9,
            match_attributes=match_attributes,
        )
