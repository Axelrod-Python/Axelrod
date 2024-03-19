"""Tests for strategies Desperate, Hopeless, Willing, and Grim."""

import axelrod as axl

from .test_player import TestPlayer

C, D = axl.Action.C, axl.Action.D


class TestDesperate(TestPlayer):

    name = "Desperate"
    player = axl.Desperate
    expected_classifier = {
        "memory_depth": 1,
        "long_run_time": False,
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Our Player (Desperate) vs Cooperator SEED --> 1
        opponent = axl.Cooperator()
        opponent_actions = [C] * 5
        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Desperate) vs Cooperator SEED --> 2
        opponent = axl.Cooperator()
        actions = [(D, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Desperate) vs Defector SEED --> 1
        opponent = axl.Defector()
        actions = [(C, D), (D, D), (C, D), (D, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Desperate) vs Defector SEED --> 2
        opponent = axl.Defector()
        actions = [(D, D), (C, D), (D, D), (C, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Desperate) vs Alternator SEED --> 1
        opponent = axl.Alternator()
        actions = [(C, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Desperate) vs Alternator SEED --> 2
        opponent = axl.Alternator()
        actions = [(D, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)


class TestHopeless(TestPlayer):

    name = "Hopeless"
    player = axl.Hopeless
    expected_classifier = {
        "memory_depth": 1,
        "long_run_time": False,
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Our Player (Hopeless) vs Cooperator SEED --> 1
        opponent = axl.Cooperator()
        opponent_actions = [C] * 5
        actions = [(C, C), (D, C), (C, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Hopeless) vs Cooperator SEED --> 2
        opponent = axl.Cooperator()
        actions = [(D, C), (C, C), (D, C), (C, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Hopeless) vs Defector SEED --> 1
        opponent = axl.Defector()
        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Hopeless) vs Defector SEED --> 2
        opponent = axl.Defector()
        actions = [(D, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Hopeless) vs Alternator SEED --> 1
        opponent = axl.Alternator()
        actions = [(C, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Hopeless) vs Alternator SEED --> 2
        opponent = axl.Alternator()
        actions = [(D, C), (C, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)


class TestWilling(TestPlayer):

    name = "Willing"
    player = axl.Willing
    expected_classifier = {
        "memory_depth": 1,
        "long_run_time": False,
        "stochastic": True,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def test_strategy(self):
        # Our Player (Willing) vs Cooperator SEED --> 1
        opponent = axl.Cooperator()
        opponent_actions = [C] * 5
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Willing) vs Cooperator SEED --> 2
        opponent = axl.Cooperator()
        actions = [(D, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Willing) vs Defector SEED --> 1
        opponent = axl.Defector()
        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Willing) vs Defector SEED --> 2
        opponent = axl.Defector()
        actions = [(D, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Willing) vs Alternator SEED --> 1
        opponent = axl.Alternator()
        actions = [(C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Willing) vs Alternator SEED --> 2
        opponent = axl.Alternator()
        actions = [(D, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)
