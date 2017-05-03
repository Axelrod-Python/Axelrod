"""Tests for strategies Desperate, Hopeless, Willing, and Grim."""
import axelrod
from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestDesperate(TestPlayer):

    name = "Desperate"
    player = axelrod.Desperate
    expected_classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)

        # Our Player (Desperate) vs Cooperator SEED --> 1
        opponent = axelrod.Cooperator()
        opponent_actions = [C] * 5
        actions = [(C, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Desperate) vs Cooperator SEED --> 2
        opponent = axelrod.Cooperator()
        actions = [(D, C), (D, C), (D, C), (D, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Desperate) vs Defector SEED --> 1
        opponent = axelrod.Defector()
        actions = [(C, D), (D, D), (C, D), (D, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Desperate) vs Defector SEED --> 2
        opponent = axelrod.Defector()
        actions = [(D, D), (C, D), (D, D), (C, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Desperate) vs Alternator SEED --> 1
        opponent = axelrod.Alternator()
        actions = [(C, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Desperate) vs Alternator SEED --> 2
        opponent = axelrod.Alternator()
        actions = [(D, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

class TestHopeless(TestPlayer):

    name = "Hopeless"
    player = axelrod.Hopeless
    expected_classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)

        # Our Player (Hopeless) vs Cooperator SEED --> 1
        opponent = axelrod.Cooperator()
        opponent_actions = [C] * 5
        actions = [(C, C), (D, C), (C, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Hopeless) vs Cooperator SEED --> 2
        opponent = axelrod.Cooperator()
        actions = [(D, C), (C, C), (D, C), (C, C), (D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Hopeless) vs Defector SEED --> 1
        opponent = axelrod.Defector()
        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Hopeless) vs Defector SEED --> 2
        opponent = axelrod.Defector()
        actions = [(D, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Hopeless) vs Alternator SEED --> 1
        opponent = axelrod.Alternator()
        actions = [(C, C), (D, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Hopeless) vs Alternator SEED --> 2
        opponent = axelrod.Alternator()
        actions = [(D, C), (C, D), (C, C), (D, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)


class TestWilling(TestPlayer):

    name = "Willing"
    player = axelrod.Willing
    expected_classifier = {
        'memory_depth': 1,
        'long_run_time': False,
        'stochastic': True,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        self.first_play_test(C, seed=1)
        self.first_play_test(D, seed=2)

        # Our Player (Willing) vs Cooperator SEED --> 1
        opponent = axelrod.Cooperator()
        opponent_actions = [C] * 5
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Willing) vs Cooperator SEED --> 2
        opponent = axelrod.Cooperator()
        actions = [(D, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Willing) vs Defector SEED --> 1
        opponent = axelrod.Defector()
        actions = [(C, D), (C, D), (C, D), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Willing) vs Defector SEED --> 2
        opponent = axelrod.Defector()
        actions = [(D, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)

        # Our Player (Willing) vs Alternator SEED --> 1
        opponent = axelrod.Alternator()
        actions = [(C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1)

        # Our Player (Willing) vs Alternator SEED --> 2
        opponent = axelrod.Alternator()
        actions = [(D, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=2)
