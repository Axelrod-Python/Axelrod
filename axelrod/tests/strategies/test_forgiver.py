"""Tests for the forgiver strategies."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestForgiver(TestPlayer):

    name = "Forgiver"
    player = axl.Forgiver
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # If opponent has defected more than 10 percent of the time, defect.
        self.versus_test(axl.Cooperator(), expected_actions=[(C, C)] * 10)

        self.versus_test(
            axl.Defector(), expected_actions=[(C, D)] + [(D, D)] * 10
        )

    def test_cooperates_if_opponent_defections_is_ten_pct_and_defects_if_opponent_defections_gt_ten_pct(
        self,
    ):
        final_action_lowers_defections_to_ten_percent = [D] + [C] * 9
        expected = [(C, D)] + [(D, C)] * 9
        self.versus_test(
            axl.MockPlayer(
                actions=final_action_lowers_defections_to_ten_percent
            ),
            expected_actions=expected * 5,
        )

    def test_never_defects_if_opponent_defections_le_ten_percent(self):
        defections_always_le_ten_percent = [C] * 9 + [D]
        expected = [(C, C)] * 9 + [(C, D)]
        self.versus_test(
            axl.MockPlayer(actions=defections_always_le_ten_percent),
            expected_actions=expected * 5,
        )


class TestForgivingTitForTat(TestPlayer):

    name = "Forgiving Tit For Tat"
    player = axl.ForgivingTitForTat
    expected_classifier = {
        "memory_depth": float("inf"),
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        self.versus_test(axl.Cooperator(), expected_actions=[(C, C)] * 5)
        self.versus_test(
            axl.Defector(), expected_actions=[(C, D)] + [(D, D)] * 5
        )
        self.versus_test(
            axl.Alternator(), expected_actions=[(C, C)] + [(C, D), (D, C)] * 5
        )

    def test_never_defects_if_opponent_defections_le_ten_percent(self):
        defections_always_le_ten_percent = [C] * 9 + [D]
        expected = [(C, C)] * 9 + [(C, D)]
        self.versus_test(
            axl.MockPlayer(actions=defections_always_le_ten_percent),
            expected_actions=expected * 5,
        )

    def test_plays_tit_for_tat_while_defections_gt_ten_percent(self):
        before_tft = (18 * [C] + [D]) * 3 + [D, D, D]
        only_cooperates = ([(C, C)] * 18 + [(C, D)]) * 3 + [
            (C, D),
            (C, D),
            (C, D),
        ]
        self.versus_test(
            axl.MockPlayer(actions=before_tft), expected_actions=only_cooperates
        )

        now_alternator = before_tft + [D, C, D, C]
        now_tft = only_cooperates + [(C, D), (D, C), (C, D), (D, C)]
        self.versus_test(
            axl.MockPlayer(actions=now_alternator), expected_actions=now_tft
        )

    def test_reverts_to_cooperator_if_defections_become_le_ten_percent(self):
        four_defections = [D, D, D, D]
        first_four = [(C, D)] + [(D, D)] * 3
        defections_at_ten_pct = four_defections + [C] * 36
        tft = first_four + [(D, C)] + [(C, C)] * 35

        maintain_ten_pct = defections_at_ten_pct + ([C] * 9 + [D]) * 3
        now_cooperates = tft + ([(C, C)] * 9 + [(C, D)]) * 3
        self.versus_test(
            axl.MockPlayer(actions=maintain_ten_pct),
            expected_actions=now_cooperates,
        )
