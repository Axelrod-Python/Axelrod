"""Tests for the Second Axelrod strategies."""

import random

import axelrod
from .test_player import TestPlayer

from axelrod.interaction_utils import compute_final_score

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


class TestTranquiliser(TestPlayer):

    name = "Tranquiliser"
    player = axelrod.Tranquiliser
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

        player = axelrod.Tranquiliser()

        self.assertEqual(player.P, 1.1)
        self.assertEqual(player.FD, 0)
        self.assertEqual(player.consecutive_defections, 0)
        self.assertEqual(player.ratio_FD1, 5)
        self.assertEqual(player.ratio_FD2, 0)
        self.assertEqual(player.ratio_FD1_count, 1)
        self.assertEqual(player.ratio_FD2_count, 1)
        self.assertEqual(player.score, None)
        self.current_score = 0

    def test_score_bad(self):

        # Tests whether TitForTat is played given score is below 1.75

        opponent = axelrod.Defector()
        actions = [(C, D)] + [(D, D)] * 20
        self.versus_test(opponent, expected_actions=actions, attrs={"P":1.1, "FD":0, "consecutive_defections":20, "ratio_FD1":5, 
                                                                    "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})

        opponent = axelrod.MockPlayer([C] * 2 + [D] * 9 + [C] * 4 )
        actions = [(C, C)] + [(C, C)] + [(C, D)] * 2 + [(D, D)] * 7 + [(D, C)] + [(C, C)] * 3  
        self.versus_test(opponent = opponent, expected_actions=actions, attrs={"P":1.8667, "FD":0, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})

        # If score is between 1.75 and 2.25, may cooperate or defect
        opponent = axelrod.MockPlayer(actions=[D] * 8 + [C] * 5 + [D])
        actions = [(C, D)] + [(D, D)] * 7 + [(D, C)] + [(C, C)] * 4
        # average_score_per_turn = 1.875
        actions += ([(C, D)]) # <-- Random
        self.versus_test(opponent, expected_actions=actions, seed=1, attrs={"P": 0.9203, "FD":0, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})

        opponent = axelrod.MockPlayer(actions=[D] * 8 + [C] * 4 + [D])
        actions = [(C, D)] + [(D, D)] * 7 + [(D, C)] + [(C, C)] * 3         
        # average_score_per_turn = 1.875
        actions += [(D, D)] # <-- Random
        self.versus_test(opponent, expected_actions=actions, seed=10, attrs={"P": 0.891, "FD":0, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})

        # If score is greater than 2.25 either cooperate or defect, if turn number <= 4; cooperate
        
        opponent = axelrod.MockPlayer(actions=[C] * 5)
        actions = [(C, C)] * 4 + [(C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=1, attrs={"P": 0.99, "FD":0, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})

        opponent = axelrod.MockPlayer(actions=[C] * 5)
        actions = [(C, C)] * 4 + [(D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=70,  attrs={"P": 0.99, "FD":1, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})

        # Given score per turn is greater than 2.25, Tranquiliser will never defect twice in a row
        
        opponent = axelrod.MockPlayer(actions = [C] * 5)
        actions = [(C, C)] * 4 + [(D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=70, attrs={"P": 0.99, "FD":1, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})
        # Tests defection probability if score == good

        opponent = axelrod.MockPlayer(actions=[C] * 5)
        actions = [(C, C)] * 4 + [(D, C)]
        self.versus_test(opponent, expected_actions=actions, seed=70, attrs={"P": 0.99, "FD":1, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1})        
       
       # Ensures FD1 values are calculated

        opponent = axelrod.MockPlayer(actions=[C] * 6)
        actions = [(C, C)] * 4 + [(D, C)] + [(C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=70, attrs={"P": 0.99, "FD":2, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":0, "ratio_FD1_count":2, "ratio_FD2_count":1})
        
        # Ensures FD2 values are calculated
        
        opponent = axelrod.MockPlayer(actions=[C] * 6)
        actions = [(C, C)] * 4 + [(D, C)] + [(C, C)] + [(C, C)]
        self.versus_test(opponent, expected_actions=actions, seed=70,  attrs={"P": 0.99, "FD":0, "consecutive_defections":0, "ratio_FD1":5, 
                                                                                "ratio_FD2":1.5, "ratio_FD1_count":2, "ratio_FD2_count":2})
        
        # Ensures scores are being counted

        opponent = axelrod.Defector()
        actions = [(C, D)] + [(D, D)] * 19
        self.versus_test(opponent, expected_actions=actions, attrs={"P": 1.1, "FD":0, "consecutive_defections":19, "ratio_FD1":5, 
                                                                    "ratio_FD2":0, "ratio_FD1_count":1, "ratio_FD2_count":1}) # Check