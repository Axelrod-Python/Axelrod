"""Tests for BackStabber and DoubleCrosser."""
import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestBackStabber(TestPlayer):

    name = "BackStabber"
    player = axelrod.BackStabber
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """
        Forgives the first 3 defections but on the fourth
        will defect forever. Defects after the 198th round unconditionally.
        """
        self._defects_after_four_defections()
        self._defects_on_last_two_rounds_by_match_len()

    def _defects_after_four_defections(self):
        self.first_play_test(C)
        # Forgives three defections
        defector_actions = [(C, D), (C, D), (C, D), (C, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=defector_actions, match_attributes={"length": 200})
        alternator_actions = [(C, C), (C, D)] * 4 + [(D, C), (D, D)] * 2
        self.versus_test(axelrod.Alternator(), expected_actions=alternator_actions, match_attributes={"length": 200})

    def _defects_on_last_two_rounds_by_match_len(self):
        actions = [(C, C)] * 198 + [(D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": 200})

        actions = [(C, C)] * 10 + [(D, C), (D, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": 12})

        # Test that exceeds tournament length
        actions = [(C, C)] * 198 + [(D, C), (D, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": 200})
        # But only if the tournament is known
        actions = [(C, C)] * 202
        self.versus_test(axelrod.Cooperator(), expected_actions=actions, match_attributes={"length": -1})


class TestDoubleCrosser(TestBackStabber):

    name = "DoubleCrosser"
    player = axelrod.DoubleCrosser
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': {'length'},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        """
        Forgives the first 3 defections but on the fourth will defect forever.
        If the opponent did not defect in the first 6 rounds the player will
        cooperate until the 180th round. Defects after the 198th round
        unconditionally.
        """

        self.special_case_strategy()
        super(TestDoubleCrosser, self).test_strategy()

    def special_case_strategy(self):

        """
        6 * [C] + 2 * [D] -> D
        6 * [C] + 20* [D] -> D
        6 * [C] + 2 * [D] + [C] - > C
        6 * [C] + 20 * [D] + [C] - > C
        """
        starting_cooperation = 6 * [C]
        starting_rounds_with_c = 6 * [(C, C)]

        starting_defection = [D] + 5 * [C]
        starting_rounds_with_d = [(D, D)] + 5 * [(C, C)]

        opponent_actions = starting_cooperation + [D, D, C]
        expected_actions = starting_rounds_with_c + [(C, D), (C, D), (D, C)]
        self.versus_test(axelrod.MockPlayer(opponent_actions), expected_actions=expected_actions,
                         match_attributes={"length": 200})

        # Defects on rounds 199, and 200 no matter what
