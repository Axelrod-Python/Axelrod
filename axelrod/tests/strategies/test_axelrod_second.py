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
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Cooperates for first 10 rounds

        actions = [(C, C), (C, D)] * 5  # Cooperate for ten rounds
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        # Mirror partner for next phase
        actions += [(D, C), (C, D)] * 7  # Mirror opponent afterwards
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        # Cooperate unless the opponent defected, has defected at least 40% of
        actions_1 = actions + [(D, C), (C, D), (C, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions_1,
                         seed=0)

        actions_2 = actions + [(D, C), (C, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions_2,
                         seed=1)

        actions_3 = actions + [(D, C), (C, D), (C, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions_3,
                         seed=2)


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


class TestGrisell(TestPlayer):
    name = "Grisell"
    player = axelrod.Grisell
    expected_classifier = {
            'memory_depth': float("inf"),
            'stochastic': False,
            'makes_use_of': set(),
            'long_run_time': False,
            'inspects_source': False,
            'manipulates_source': False,
            'manipulates_state': False
            }

    def test_strategy(self):
        # If the ratio of opponent defections to matches is less than 0.5 then cooporate
        opponent = axelrod.Cooperator()
        actions = [(C, C)] * 20
        self.versus_test(opponent, expected_actions=actions)

        opponent = axelrod.Defector()
        actions = [(C, D), (D, D)]
        self.versus_test(opponent, expected_actions=actions)

        opponent_actions = (D, D, D, D, C, C, C, C, C, C)
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, D), (D, D), (D, D), (D, D), (D, C), (D, C), (D, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)


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

class TestTranquilizer(TestPlayer):

    name = "Tranquilizer"
    player = axelrod.Tranquilizer
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': {"game"},
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    # test for initalised variables

    def test_init(self):

        player = axelrod.Tranquilizer()

        self.assertEqual(player.num_turns_after_good_defection, 0)
        self.assertEqual(player.opponent_consecutive_defections, 0)
        self.assertEqual(player.one_turn_after_good_defection_ratio, 5)
        self.assertEqual(player.two_turns_after_good_defection_ratio, 0)
        self.assertEqual(player.one_turn_after_good_defection_ratio_count, 1)
        self.assertEqual(player.two_turns_after_good_defection_ratio_count, 1)

    def test_strategy(self):

        opponent = axelrod.Bully()
        actions = [(C, D), (D, D), (D, C), (C, C), (C, D), (D, D), (D, C), (C, C)]
        expected_attrs={"num_turns_after_good_defection": 0,
                        "one_turn_after_good_defection_ratio": 5,
                        "two_turns_after_good_defection_ratio": 0,
                        "one_turn_after_good_defection_ratio_count": 1,
                        "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions,
                         attrs=expected_attrs)

        # Tests whether TitForTat is played given score is below 1.75

        opponent = axelrod.Defector()
        actions = [(C, D)] + [(D, D)] * 20
        expected_attrs={"num_turns_after_good_defection": 0,
                        "one_turn_after_good_defection_ratio": 5,
                        "two_turns_after_good_defection_ratio": 0,
                        "one_turn_after_good_defection_ratio_count": 1,
                        "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions,
                         attrs=expected_attrs)

        opponent = axelrod.MockPlayer([C] * 2 + [D] * 8 + [C] * 4 )
        actions = [(C, C), (C, C)] + [(C, D)] + [(D, D)] * 7 + [(D, C)] + [(C, C)] * 3
        expected_attrs={"num_turns_after_good_defection": 0,
                        "one_turn_after_good_defection_ratio": 5,
                        "two_turns_after_good_defection_ratio": 0,
                        "one_turn_after_good_defection_ratio_count": 1,
                        "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions,
                         attrs=expected_attrs)

        # If score is between 1.75 and 2.25, may cooperate or defect

        opponent = axelrod.MockPlayer(actions=[D] * 3 + [C] * 4 + [D] * 2)
        actions = [(C, D)] + [(D, D)] * 2 + [(D, C)] + [(C, C)] * 3 + [(C, D)]
        actions += ([(C, D)]) # <-- Random
        expected_attrs={"num_turns_after_good_defection": 0,
               "one_turn_after_good_defection_ratio": 5,
               "two_turns_after_good_defection_ratio": 0,
               "one_turn_after_good_defection_ratio_count": 1,
               "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions, seed=0,
                         attrs=expected_attrs)

        opponent = axelrod.MockPlayer(actions=[D] * 3 + [C] * 4 + [D] * 2)
        actions = [(C, D)] + [(D, D)] * 2 + [(D, C)] + [(C, C)] * 3 + [(C, D)]
        actions += ([(D, D)]) # <-- Random
        expected_attrs={"num_turns_after_good_defection": 0,
                  "one_turn_after_good_defection_ratio": 5,
                  "two_turns_after_good_defection_ratio": 0,
                  "one_turn_after_good_defection_ratio_count": 1,
                  "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions, seed=17,
                         attrs=expected_attrs)

        """If score is greater than 2.25 either cooperate or defect,
           if turn number <= 5; cooperate"""

        opponent = axelrod.MockPlayer(actions=[C] * 5)
        actions = [(C, C)] * 5
        expected_attrs={"num_turns_after_good_defection": 0,
                "one_turn_after_good_defection_ratio": 5,
                "two_turns_after_good_defection_ratio": 0,
                "one_turn_after_good_defection_ratio_count": 1,
                "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions, seed=1,
                         attrs=expected_attrs)

        opponent = axelrod.MockPlayer(actions=[C] * 5)
        actions = [(C, C)] * 4 + [(D, C)]
        expected_attrs={"num_turns_after_good_defection": 1,
                "one_turn_after_good_defection_ratio": 5,
                "two_turns_after_good_defection_ratio": 0,
                "one_turn_after_good_defection_ratio_count": 1,
                "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions, seed=89,
                         attrs=expected_attrs)

        """ Given score per turn is greater than 2.25,
            Tranquilizer will never defect twice in a row"""

        opponent = axelrod.MockPlayer(actions = [C] * 6)
        actions = [(C, C)] * 4 + [(D, C), (C, C)]
        expected_attrs={"num_turns_after_good_defection": 2,
                 "one_turn_after_good_defection_ratio": 5,
                 "two_turns_after_good_defection_ratio": 0,
                 "one_turn_after_good_defection_ratio_count": 2,
                 "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions, seed=89,
                         attrs=expected_attrs)

        # Tests cooperation after update_state

        opponent = axelrod.MockPlayer(actions=[C] * 5)
        actions = [(C, C)] * 4 + [(D, C)] + [(C, C)]
        expected_attrs={"num_turns_after_good_defection": 2,
                "one_turn_after_good_defection_ratio": 5,
                "two_turns_after_good_defection_ratio": 0,
                "one_turn_after_good_defection_ratio_count": 2,
                "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions, seed=89,
                         attrs=expected_attrs)

       # Ensures FD1 values are calculated

        opponent = axelrod.MockPlayer(actions=[C] * 6)
        actions = [(C, C)] * 4 + [(D, C), (C, C)]
        expected_attrs={"num_turns_after_good_defection": 2,
                "one_turn_after_good_defection_ratio": 5,
                "two_turns_after_good_defection_ratio": 0,
                "one_turn_after_good_defection_ratio_count": 2,
                "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions, seed=89,
                         attrs=expected_attrs)

        # Ensures FD2 values are calculated

        opponent = axelrod.MockPlayer(actions=[C] * 6)
        actions = [(C, C)] * 4 + [(D, C)] + [(C, C)] * 2
        expected_attrs={"num_turns_after_good_defection": 0,
                 "one_turn_after_good_defection_ratio": 5,
                 "two_turns_after_good_defection_ratio": 1.5,
                 "one_turn_after_good_defection_ratio_count": 2,
                 "two_turns_after_good_defection_ratio_count": 2}
        self.versus_test(opponent, expected_actions=actions, seed=89,
                         attrs=expected_attrs)

        # Ensures scores are being counted

        opponent = axelrod.Defector()
        actions = [(C, D)] + [(D, D)] * 19
        expected_attrs={"num_turns_after_good_defection": 0,
                "one_turn_after_good_defection_ratio": 5,
                "two_turns_after_good_defection_ratio": 0,
                "one_turn_after_good_defection_ratio_count": 1,
                "two_turns_after_good_defection_ratio_count": 1}
        self.versus_test(opponent, expected_actions=actions,
                         attrs=expected_attrs)


class TestMoreGrofman(TestPlayer):

    name = "MoreGrofman"
    player = axelrod.MoreGrofman
    expected_classifier = {
        'memory_depth': 8,
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
        # Own previous move was C, opponent defected less than 3 times in last 8
        moregrofman_actions = [C] * 7 + [C]
        opponent_actions = [C] * 6 + [D] * 2
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Own previous move was C, opponent defected 3 or more times in last 8
        moregrofman_actions = ([C] * 3 + [D] * 3 + [C]) + [D]
        opponent_actions = ([C] * 2 + [D] * 3 + [C] * 2) + [D]
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Own previous move was D, opponent defected once or less in last 8
        moregrofman_actions = ([C] * 6 + [D]) + [C]
        opponent_actions = ([C] * 5 + [D] * 1 + [C]) + [D]
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Own previous move was D, opponent defected more than once in last 8
        moregrofman_actions = ([C] * 2 + [D] * 5) + [D]
        opponent_actions = ([D] * 7) + [D]
        opponent = axelrod.MockPlayer(actions=opponent_actions)
        actions = list(zip(moregrofman_actions, opponent_actions))
        self.versus_test(opponent, expected_actions=actions)

        # Test to make sure logic matches Fortran (discrepancy found 8/23/2017)
        opponent = axelrod.AntiTitForTat()
        # Actions come from a match run by Axelrod Fortran using Player('k86r')
        actions = [(C, C), (C, D), (D, D), (D, C), (C, C), (C, D), (D, D),
            (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (C, C)]
        self.versus_test(opponent, expected_actions=actions)

        # Test to match the Fortran implementation for 30 rounds
        opponent = axelrod.AntiTitForTat()
        actions = [(C, C), (C, D), (D, D), (D, C), (C, C), (C, D), (D, D),
            (D, C),  (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (C, C),
            (C, D), (C, D), (C, D), (C, D), (D, D), (D, C), (D, C), (D, C),
            (D, C), (D, C), (D, C), (D, C), (C, C), (C, D), (C, D)]
        self.versus_test(opponent, expected_actions=actions)

        # Test to match the Fortran implementation for 60 rounds
        opponent = axelrod.AntiTitForTat()
        actions = [(C, C), (C, D), (D, D), (D, C), (C, C), (C, D), (D, D),
            (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (C, C),
            (C, D), (C, D), (C, D), (C, D), (D, D), (D, C), (D, C), (D, C),
            (D, C), (D, C), (D, C), (D, C), (C, C), (C, D), (C, D), (C, D),
            (C, D), (D, D), (D, C), (D, C), (D, C), (D, C), (D, C), (D, C),
            (D, C), (C, C), (C, D), (C, D), (C, D), (C, D), (D, D), (D, C),
            (D, C), (D, C), (D, C), (D, C), (D, C), (D, C), (C, C), (C, D),
            (C, D), (C, D), (C, D), (D, D), (D, C)]
        self.versus_test(opponent, expected_actions=actions)
