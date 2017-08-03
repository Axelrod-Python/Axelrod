"""Tests for the retaliate strategy."""

import axelrod
from .test_player import TestPlayer, TestOpponent

C, D = axelrod.Action.C, axelrod.Action.D


class TestRetaliate(TestPlayer):

    name = "Retaliate: 0.1"
    player = axelrod.Retaliate
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent has defected more than 10 percent of the time, defect.
        opponent = axelrod.Cooperator()
        actions = [(C, C)] * 5
        self.versus_test(opponent=opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer([C, C, C, D, C])
        actions = [(C, C), (C, C), (C, C), (C, D), (D, C), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)


class TestRetaliate2(TestPlayer):

    name = "Retaliate 2: 0.08"
    player = axelrod.Retaliate2
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent has defected more than 8 percent of the time, defect.
        opponent = axelrod.MockPlayer([C] * 13 + [D])
        actions = [(C, C)] * 13 + [(C, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)


class TestRetaliate3(TestPlayer):

    name = "Retaliate 3: 0.05"
    player = axelrod.Retaliate3
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent has defected more than 5 percent of the time, defect.
        opponent = axelrod.MockPlayer([C] * 19 + [D])
        actions = [(C, C)] * 19 + [(C, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions)


class TestLimitedRetaliate(TestPlayer):

    name = 'Limited Retaliate: 0.1, 20'
    player = axelrod.LimitedRetaliate
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # If opponent has never defected, co-operate
        opponent = axelrod.Cooperator()
        actions = [(C, C)] * 5
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"retaliating": False})

        # Retaliate after a (C, D) round.
        opponent = axelrod.MockPlayer([C, C, C, D, C])
        actions = [(C, C), (C, C), (C, C), (C, D), (D, C), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"retaliating": True})

        opponent = axelrod.Alternator()

        # Count retaliations
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"retaliation_count": 3})
        opponent = axelrod.Alternator()

        # Cooperate if we hit the retaliation limit
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C)]
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"retaliation_count": 0},
                         init_kwargs={"retaliation_limit": 2})

        # Defect again after cooperating
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (D, D), (D, C)]
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"retaliation_count": 2},
                         init_kwargs={"retaliation_limit": 2})

        # Different behaviour with different retaliation threshold
        actions = [(C, C), (C, D), (D, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=opponent, expected_actions=actions,
                         attrs={"retaliation_count": 0},
                         init_kwargs={"retaliation_limit": 2,
                                      "retaliation_threshold": 9})
