"""Tests for the Second Axelrod strategies."""

import random

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestChampion(TestPlayer):
    name = "Champion"
    player = axelrod.Champion
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(["length"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperates for num_rounds / 20 (10 by default)

        actions = [(C, C), (C, D)] * 5  # Cooperate for ten rounds
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         match_attributes={"length": 200})

        # Mirror partner for next phase
        actions += [(D, C), (C, D)] * 7  # Mirror opponent afterwards
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         match_attributes={"length": 200})

        # Cooperate unless the opponent defected, has defected at least 40% of
        actions_1 = actions + [(D, C), (C, D), (C, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions_1,
                         match_attributes={"length": 200}, seed=0)

        actions_2 = actions + [(D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions_2,
                         match_attributes={"length": 200}, seed=1)

        actions_3 = actions + [(D, C), (C, D), (C, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions_3,
                         match_attributes={"length": 200}, seed=2)


class TestEatherley(TestPlayer):

    name = "Eatherley"
    player = axelrod.Eatherley
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
        # Test cooperate after opponent cooperates
        actions = [(C, C)] * 5
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # If opponent only defects then probability of cooperating is 0.
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        # Stochastic response to defect
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         seed=0)
        actions = [(C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         seed=1)

        opponent = axelrod.MockPlayer(actions=[D, C, C, D])
        actions = [(C, D), (D, C), (C, C), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions, seed=8)
        opponent = axelrod.MockPlayer(actions=[D, C, C, D])
        actions = [(C, D), (D, C), (C, C), (C, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions, seed=2)


class TestTester(TestPlayer):

    name = "Tester"
    player = axelrod.Tester
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
        # Alternate after 3rd round if opponent only cooperates
        actions = [(D, C)] + [(C, C), (C, C)] + [(D, C), (C, C)] * 4
        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
                         attrs={"is_TFT": False})

        # Cooperate after initial defection and become TfT
        actions = [(D, C), (C, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         attrs={"is_TFT": True})

        # Now play TfT
        opponent = axelrod.MockPlayer(actions=[C, D, C, D, D, C])
        actions = [(D, C), (C, D), (C, C), (C, D), (D, D), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={"is_TFT": True})


class TestGladstein(TestPlayer):

    name = "Gladstein"
    player = axelrod.Gladstein
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
        # Cooperates and begins to play TFT when Alternator defects
        actions = [(D, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions,
                         attrs={'patsy': False})

        # Cooperation ratio will always be less than 0.5
        actions = [(D, C), (C, C), (C, C), (D, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions,
                         attrs={'patsy': True})

        # Apologizes immediately and plays TFT
        actions = [(D, D), (C, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions,
                         attrs={'patsy': False})

        # Ratio is 1/3 when MockPlayer defected for the first time.
        opponent = axelrod.MockPlayer(actions=[C, C, C, D, D])
        actions = [(D, C), (C, C), (C, C), (D, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={'patsy': False})

        opponent = axelrod.AntiTitForTat()
        actions = [(D, C), (C, C), (C, D), (C, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions,
                         attrs={'patsy': False})


class TestMoreGrofman(TestPlayer):

    name = "MoreGrofman"
    player = axelrod.MoreGrofman
    expected_classifier = {
        'memory_depth': 7,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperate for the first two rounds
        actions = [(C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # Cooperate for the first two rounds, then play tit for tat for 3-7
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        # Demonstrate MoreGrofman Logic
        # Own previous move was C, opponent defected less than twice in last 7
        moregrofman_actions = [C] * 7 + [C]
        opponent_actions = [C] * 6 + [D] * 2
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Own previous move was C, opponent defected more than twice in last 7
        moregrofman_actions = ([C] * 3 + [D] * 3 + [C]) + [D]
        opponent_actions = ([C] * 2 + [D] * 3 + [C] * 2) + [D]
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Own previous move was D, opponent defected once in last 7
        moregrofman_actions = ([C] * 6 + [D]) + [C]
        opponent_actions = ([C] * 5 + [D] * 1 + [C]) + [D]
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Own previous move was D, opponent defected more than twice in last 7
        moregrofman_actions = ([C] * 2 + [D] * 5) + [D]
        opponent_actions = ([D] * 7) + [D]
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Test to make sure logic matches Fortran (discrepancy found 8/23/2017)
        opponent = axelrod.AntiTitForTat()
        # Actions come from a match run by Axelrod Fortran using Player('k86r')
        actions = [
            (C, C),
            (C, D),
            (D, D),
            (D, C),
            (C, C),
            (C, D),
            (D, D),
            (D, C),
            (D, C),
            (D, C),
            (D, C),
            (D, C),
            (D, C),
            (D, C), # element 13
            (C, C)
            ]
        self.versus_test(opponent, expected_actions=actions)

        # Test to match the Fortran implementation for 30 rounds
        # opponent = axelrod.AntiTitForTat()
        # actions = [(C, C), (C, D), (D, D), (D, C), (C, C), (C, D), (D, D),
        #     (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (C, C),
        #     (C, D), (C, D), (C, D), (C, D), (D, D), (D, C), (D, C), (D, C),
        #     (D, C), (D, C), (D, C), (D, C), (C, C), (C, D), (C, D)]
        # self.versus_test(opponent, expected_actions=actions)
