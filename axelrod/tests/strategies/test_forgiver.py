"""Tests for the forgiver strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestForgiver(TestPlayer):

    name = "Forgiver"
    player = axelrod.Forgiver
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        # If opponent has defected more than 10 percent of the time, defect.
        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)] * 10)

        self.versus_test(axelrod.Defector(), expected_actions=[(C, D)] + [(D, D)] * 10)

    def test_cooperates_if_opponent_defections_is_ten_pct_and_defects_if_opponent_defections_gt_ten_pct(self):
        final_action_lowers_defections_to_ten_percent = [D] + [C] * 9
        expected = [(C, D)] + [(D, C)] * 9
        self.versus_test(axelrod.MockPlayer(actions=final_action_lowers_defections_to_ten_percent),
                         expected_actions=expected * 5)

    def test_never_defects_if_opponent_defections_le_ten_percent(self):
        defections_always_le_ten_percent = [C] * 9 + [D]
        expected = [(C, C)] * 9 + [(C, D)]
        self.versus_test(axelrod.MockPlayer(actions=defections_always_le_ten_percent), expected_actions=expected * 5)


class TestForgivingTitForTat(TestPlayer):

    name = "Forgiving Tit For Tat"
    player = axelrod.ForgivingTitForTat
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)

        self.versus_test(axelrod.Cooperator(), expected_actions=[(C, C)] * 5)
        self.versus_test(axelrod.Defector(), expected_actions=[(C, D)] + [(D, D)] * 5)
        self.versus_test(axelrod.Alternator(), expected_actions=[(C, C)] + [(C, D), (D, C)] * 5)

    def test_never_defects_if_opponent_defections_le_ten_percent(self):
        defections_always_le_ten_percent = [C] * 9 + [D]
        expected = [(C, C)] * 9 + [(C, D)]
        self.versus_test(axelrod.MockPlayer(actions=defections_always_le_ten_percent), expected_actions=expected * 5)

    def plays_tit_for_tat_while_defections_gt_ten_percent(self):
        before_tft = (19 * [C] + [D]) * 3 + [D, D, D]
        only_cooperates = ([(C, C)] * 19 + [(C, D)]) * 3 + [(D, D), (D, D), (D, D)]
        self.versus_test(axelrod.MockPlayer(actions=before_tft), expected_actions=only_cooperates)

        now_alternator = before_tft + [C, D, C, D, C]
        now_tft = only_cooperates + [(D, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.MockPlayer(actions=now_alternator), expected_actions=now_tft)

    def reverts_to_cooperator_if_defections_become_le_ten_percent(self):
        four_defections = [D, D, D, D]
        first_four = [(C, D)] + [(D, D)] * 3
        defections_at_ten_pct = four_defections + [C] * 3
        tft = first_four + [(D, C)] + [(C, C)] * 36

        maintain_ten_pct = defections_at_ten_pct + ([C] * 9 + [D]) * 3
        now_cooperates = tft + [(C, C)] * 30
        self.versus_test(axelrod.MockPlayer(actions=maintain_ten_pct), expected_actions=now_cooperates)
