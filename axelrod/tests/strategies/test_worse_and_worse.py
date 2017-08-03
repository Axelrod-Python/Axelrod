"""Tests for the WorseAndWorse strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D

class TestWorseAndWorse(TestPlayer):

    name = "Worse and Worse"
    player = axelrod.WorseAndWorse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that the strategy gives expected behaviour."""
        # 6 Rounds Cooperate given seed
        actions = [(C, C)] * 6 + [(D, C)] + [(C, C)] * 3
        self.versus_test(axelrod.Cooperator(), expected_actions = actions,
                         seed=8)

       # 6 Rounds Cooperate and Defect no matter oponent
        actions = [(C, D)] * 6 + [(D, D)] + [(C, D)] * 3
        self.versus_test(axelrod.Defector(), expected_actions = actions,
                         seed=8)


class TestWorseAndWorseRandom(TestPlayer):

    name = "Knowledgeable Worse and Worse"
    player = axelrod.KnowledgeableWorseAndWorse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that the strategy gives expected behaviour."""
        actions = [(C, C)] + [(D, C)] * 4
        self.versus_test(axelrod.Cooperator(), expected_actions = actions,
                         match_attributes={"length":5}, seed=1)

        # Test that behaviour does not depend on opponent
        actions = [(C, D)] + [(D, D)] * 4
        self.versus_test(axelrod.Defector(), expected_actions = actions,
                         match_attributes={"length":5}, seed=1)

        # Test that behaviour changes when does not know length.
        actions = [(C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_actions = actions,
                         match_attributes={"length":-1}, seed=1)


class TestWorseAndWorse2(TestPlayer):

    name = "Worse and Worse 2"
    player = axelrod.WorseAndWorse2
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that the strategy gives expected behaviour."""

        # Test next move matches opponent
        actions = [(C, C)] * 19
        self.versus_test(axelrod.Cooperator(), expected_actions = actions)

        actions = [(C, C), (C, C), (C, D),(D, C)]
        self.versus_test(opponent=axelrod.MockPlayer(actions=[C,C,D,C]), expected_actions = actions)

        actions = [(C, C)] * 18 + [(C, D), (D, C)]
        self.versus_test(opponent=axelrod.MockPlayer(actions=[C] * 18 + [D, C]), expected_actions = actions)

        # After round 20, strategy follows stochastic behavior given a seed
        actions = [(C, C)] * 20 + [(C, D), (D, C), (C, C), (C, D)]
        self.versus_test(opponent=axelrod.MockPlayer(actions=[C] * 20 + [D, C, C, D]), expected_actions = actions,
                         seed=8)

        actions = [(C, C)] * 20 + [(D, D), (D, C)] + [(C, C)] * 2 + [(D, C)]
        self.versus_test(opponent=axelrod.MockPlayer(actions=[C] * 20 + [D, C, C, C]), expected_actions = actions,
                         seed=2)


class TestWorseAndWorse3(TestPlayer):

    name = "Worse and Worse 3"
    player = axelrod.WorseAndWorse3
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that the strategy gives expected behaviour."""
        # Test that if opponent only defects, strategy also defects
        actions = [(C, D)] + [(D, D)] * 4
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        # Test that if opponent only cooperates, strategy also cooperates
        actions = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # Test that given a non 0/1 probability of defecting, strategy follows
        # stochastic behaviour, given a seed
        actions = [(C, C), (C, D), (C, C), (D, D), (C, C), (D, C)]
        self.versus_test(axelrod.MockPlayer(actions=[C,D,C,D,C]), expected_actions=actions, seed=8)
