"""Tests for the Second Axelrod strategies."""

import random
import numpy as np

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


class TestKluepfel(TestPlayer):
    name = "Kluepfel"
    player = axelrod.Kluepfel
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
        actions = [(C, C)] * 100  # Cooperate forever
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # Since never two in a row, will respond in kind with 70% if
        # coop and 60% otherwise, after first couple
        actions = [(C, C),
                    (C, D), # Views first three as the same.
                    # A random gets used in each of the first two.
                    (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions, seed=1)

        actions = [(C, C), (C, D),
                    (C, C), (D, D), (D, C), (C, D)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions, seed=2)

        actions = [(C, C), (C, D),
                    (D, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions, seed=3)

        # Now we have to test the detect-random logic, which doesn't pick up
        # until after 26 turns.  So we need a big sample.
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D), (D, C), (C, C),
                   (C, D), (C, C), (D, D), (D, C), (C, C), (C, D), (D, D),
                   (C, D), (D, D), (D, C), (C, C), (D, C), (C, C), (C, D),
                   (D, D), (D, C), (C, D), (D, C), (C, C), (C, D),
                    # Success detect random opponent for remaining turns.
                   (D, D), (D, D), (D, D), (D, C), (D, D), (D, C), (D, D),
                   (D, C), (D, D), (D, C), (D, C), (D, D), (D, D), (D, C),
                   (D, C), (D, C), (D, C), (D, D), (D, C), (D, C), (D, C),
                   (D, C), (D, D)]
        self.versus_test(axelrod.Random(0.5), expected_actions=actions, seed=10)


class TestBorufsen(TestPlayer):
    name = "Borufsen"
    player = axelrod.Borufsen
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
        actions = [(C, C)] * 100  # Cooperate forever
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # Tries to cooperate every third time until detecting defective
        actions = [(C, D), (D, D), (D, D), (D, D)] * 6 + \
                    [(C, D), (D, D)] + [(D, D)] * 100
        self.versus_test(axelrod.Defector(), expected_actions=actions)

        # Alternates with additional coop, every sixth turn
        # Won't be labeled as random, since 2/3 of opponent's C follow
        # player's C
        # `flip_next_defect` will get set on the sixth turn, which changes the
        # seventh action
        # Note that the first two turns of each period of six aren't
        #  marked as echoes, and the third isn't marked that way until the
        # fourth turn.
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)] * 20
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        # Basically does tit-for-tat against Win-Shift, Lose-Stay D
        # After 26 turns, will detect random since half of opponent's C follow
        # Cs
        # Coming out of it, there will be new pattern.  Then random is detected
        # again.
        actions = [(C, D), (D, C), (C, C)] * 8 + \
                    [(C, D), (D, C)] + [(D, C)] * 25 + \
                    [(D, C)] + [(C, C), (C, D), (D, C)] * 8 + \
                    [(D, C)] * 25
        self.versus_test(axelrod.WinShiftLoseStay(D), expected_actions=actions)


class TestCave(TestPlayer):
    name = "Cave"
    player = axelrod.Cave
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
        actions = [(C, C)] * 100
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # It will take until turn 18 to respond decide to repond D->D
        actions = [(C, D)]
        actions += [(C, D), (D, D), (D, D), (C, D), (C, D), (C, D), (D, D),
                    (D, D), (C, D), (C, D), (D, D), (C, D), (D, D), (C, D),
                    (C, D), (D, D), (C, D)] # Randomly choose
        actions += [(D, D)] * 30 # Defect
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=1)

        # Highly-defective opponent
        # It will take until turn 20 to respond decide to repond D to C
        opponent_actions = [D] * 17 + [C, C, C, C]
        almost_defector = axelrod.MockPlayer(actions=opponent_actions)

        actions = [(C, D)]
        actions += [(C, D), (D, D), (D, D), (C, D), (C, D), (C, D), (D, D),
                    (D, D), (C, D), (C, D), (D, D), (C, D), (D, D), (C, D),
                    (C, D), (D, D), (C, C)] # Randomly choose
        actions += [(C, C)] # Coop for a minute
        actions += [(D, C), (D, C)]
        self.versus_test(almost_defector, expected_actions=actions, seed=1)

        #Here it will take until turn 40 to detect random and defect
        actions = [(C, C)]
        actions += [(C, D), (D, C), (C, D), (D, C), (C, D), (C, C), (C, D),
                    (C, C), (C, D), (D, C), (C, D), (D, C), (C, D), (D, C),
                    (C, D), (C, C), (C, D), (D, C), (C, D), (D, C), (C, D),
                    (D, C), (C, D), (C, C), (C, D), (C, C), (C, D), (C, C),
                    (C, D), (D, C), (C, D), (D, C), (C, D), (D, C), (C, D)] #Randomly choose
        actions += [(D, C), (C, D), (D, C)] # 17 D have come, so tit for tat for a while
        actions += [(D, D), (D, C)] * 100 # Random finally detected
        self.versus_test(axelrod.Alternator(), expected_actions=actions, seed=2)


class TestWmAdams(TestPlayer):
    name = "WmAdams"
    player = axelrod.WmAdams
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
        actions = [(C, C)] * 100  # Cooperate forever
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # Will ignore the first four defects
        opponent_actions = [D] * 4 + [C] * 100
        defect_four = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, D)] * 4 + [(C, C)] * 100
        self.versus_test(defect_four, expected_actions=actions)

        actions = [(C, D), (C, D), (C, D), (C, D), (C, D), (D, D), (C, D),
                   (C, D), (D, D), (C, D), (D, D), (C, D), (D, D), (D, D),
                   (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=1)
        actions = [(C, D), (C, D), (C, D), (C, D), (C, D), (D, D), (C, D),
                   (C, D), (D, D), (C, D), (D, D), (D, D), (D, D), (C, D),
                   (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions, seed=2)

        # After responding to the 11th D (counted as 10 D), just start cooperating
        opponent_actions = [D] * 11 + [C] * 100
        changed_man = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, D), (C, D), (C, D), (C, D), (C, D), (D, D), (C, D),
                   (C, D), (D, D), (C, D), (D, D), (C, C)]
        actions += [(C, C)] * 99
        self.versus_test(changed_man, expected_actions=actions, seed=1)


class TestGraaskampKatzen(TestPlayer):
    name = "GraaskampKatzen"
    player = axelrod.GraaskampKatzen
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C)] * 100  # Cooperate forever
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        # GK does not great against
        opponent_actions = [C, D, D] * 100
        GK_Foil = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, C), (C, D), (D, D)]
        actions += [(D, C), (C, D), (D, D)] * 2
        actions += [(D, C)]
        actions += [(D, D), (D, D), (D, C)] * 20 # Defect here on
        self.versus_test(GK_Foil, expected_actions=actions)

        # Fail on second checkpoint
        opponent_actions = [C] * 10 + [C, D, D] * 100
        Delayed_GK_Foil = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, C)] * 10
        actions += [(C, C), (C, D), (D, D)]
        actions += [(D, C), (C, D), (D, D)] * 2
        actions += [(D, C)]
        actions += [(D, D), (D, D), (D, C)] * 20 # Defect here on
        self.versus_test(Delayed_GK_Foil, expected_actions=actions)


class TestWeiner(TestPlayer):
    name = "Weiner"
    player = axelrod.Weiner
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
        actions = [(C, C)] * 100  # Cooperate forever
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, C)]
        actions += [(C, D), (D, C)] # Tit-for-Tat
        # Opponent's last move was a C with 1 D between
        actions += [(C, D)] # Tit-for-Tat. Raise forgiveness flag.
        actions += [(C, C)] # Tit-for-Tat. Use forgiveness flag.
        # Opponent's last move was a C, but defect_padding counted as 0.
        actions += [(C, D), (D, C)] # Tit-for-Tat
        # Opponent's last move was a C with 1 D between
        actions += [(C, D)] # Tit-for-Tat. Raise forgiveness flag.
        actions += [(D, C)] # Tit-for-Tat. Try forgiveness flag.
        # This time grudge=20, so the forgiveness flag doesn't work.
        actions += [(C, D)] # Tit-for-Tat.
        # This is the 5th opponent defect, won't be counted for 2 turns
        actions += [(D, C)] # Tit-for-Tat.
        actions += [(D, D), (D, C)] * 100 # Defect now on.
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        # Build an opponent that will cause a wasted flag.
        opponent_actions = [C, D, C, C, C, C, D, D]
        Flag_Waster_1 = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, C), (C, D), (D, C)]
        actions += [(C, C)] # Raise flag, like in Alternator
        actions += [(C, C)] # Use flag, but don't change outcome
        actions += [(C, C)]
        actions += [(C, D)] # Don't raise flag
        actions += [(D, D)] # Don't use flag
        self.versus_test(Flag_Waster_1, expected_actions=actions)

        # Demonstrate that grudge is not incremented on wasted flag.
        opponent_actions = [C, D, C, C, C, C, D, C, D, C]
        Flag_Waster_2 = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, C), (C, D), (D, C)]
        actions += [(C, C)] # Raise flag, like in Alternator
        actions += [(C, C)] # Use flag, but don't change outcome
        actions += [(C, C), (C, D), (D, C)]
        actions += [(C, D)] # Raise flag
        actions += [(C, C)] # Use flag to change outcome
        self.versus_test(Flag_Waster_2, expected_actions=actions)

        # Show grudge passing over time
        opponent_actions = [C, D, C, D, C] + [C] * 11 + [C, D, C, D, C]
        Time_Passer = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, C), (C, D), (D, C)]
        actions += [(C, D)] # Raise flag
        actions += [(C, C)] # Use flag to change outcome
        actions += [(C, C)] * 11
        actions += [(C, C), (C, D), (D, C)]
        actions += [(C, D)] # Raise flag
        actions += [(C, C)] # Use flag to change outcome
        self.versus_test(Time_Passer, expected_actions=actions)


class TestHarrington(TestPlayer):
    name = "Harrington"
    player = axelrod.Harrington
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
        # Build an opponent that will cooperate the first 36 turns and
        # defect on the 37th turn
        opponent_actions = [C] * 36 + [D] + [C] * 100
        Defect37 = axelrod.MockPlayer(actions=opponent_actions)
        # Activate the Fair-weather flag
        actions = [(C, C)] * 36 + [(D, D)] + [(C, C)] * 100
        self.versus_test(Defect37, expected_actions=actions, attrs={"mode": "Fair-weather"})

        # Defect on 37th turn to activate Fair-weather, then later defect to
        # exit Fair-weather
        opponent_actions = [C] * 36 + [D] + [C] * 100 + [D] + [C] * 4
        Defect37_big = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, C)] * 36 + [(D, D)] + [(C, C)] * 100
        actions += [(C, D)]
        #Immediately exit Fair-weather
        actions += [(D, C), (C, C), (D, C), (C, C)]
        self.versus_test(Defect37_big, expected_actions=actions, seed=2, attrs={"mode": "Normal"})
        actions = [(C, C)] * 36 + [(D, D)] + [(C, C)] * 100
        actions += [(C, D)]
        #Immediately exit Fair-weather
        actions += [(D, C), (C, C), (C, C), (C, C)]
        self.versus_test(Defect37_big, expected_actions=actions, seed=1, attrs={"mode": "Normal"})

        # Opponent defects on 1st turn
        opponent_actions = [D] + [C] * 46
        Defect1 = axelrod.MockPlayer(actions=opponent_actions)
        # Tit-for-Tat on the first, but no streaks, no Fair-weather flag.
        actions = [(C, D), (D, C)] + [(C, C)] * 34 + [(D, C)]
        # Two cooperations scheduled after the 37-turn defection
        actions += [(C, C)] * 2
        # TFT twice, then random number yields a DCC combo.
        actions += [(C, C)] * 2
        actions += [(D, C), (C, C), (C, C)]
        # Don't draw next random number until now.  Again DCC.
        actions += [(D, C), (C, C), (C, C)]
        self.versus_test(Defect1, expected_actions=actions, seed=2)

        # Defection on turn 37 by opponent doesn't have an effect here
        opponent_actions = [D] + [C] * 35 + [D] + [C] * 10
        Defect1_37 = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, D), (D, C)] + [(C, C)] * 34 + [(D, D)]
        actions += [(C, C)] * 2
        actions += [(C, C)] * 2
        actions += [(D, C), (C, C), (C, C)]
        actions += [(D, C), (C, C), (C, C)]
        self.versus_test(Defect1_37, expected_actions=actions, seed=2)

        # However a defect on turn 38 would be considered a burn.
        opponent_actions = [D] + [C] * 36 + [D] + [C] * 9
        Defect1_38 = axelrod.MockPlayer(actions=opponent_actions)
        # Tit-for-Tat on the first, but no streaks, no Fair-weather flag.
        actions = [(C, D), (D, C)] + [(C, C)] * 34 + [(D, C)]
        # Two cooperations scheduled after the 37-turn defection
        actions += [(C, D), (C, C)]
        # TFT from then on, since burned
        actions += [(C, C)] * 8
        self.versus_test(Defect1_38, expected_actions=actions, seed=2, attrs={"burned": True})

        # Use alternator to test parity flags.
        actions = [(C, C), (C, D)]
        # Even streak is set to 2, one for the opponent's defect and one for
        # our defect.
        actions += [(D, C)]
        actions += [(C, D)]
        # Even streak is increased two more.
        actions += [(D, C)]
        actions += [(C, D)]
        # Opponent's defect increments even streak to 5, so we cooperate.
        actions += [(C, C)]
        actions += [(C, D), (D, C), (C, D), (D, C), (C, D)]
        # Another 5 streak
        actions += [(C, C)]
        # Repeat
        actions += [(C, D), (D, C), (C, D), (D, C), (C, D), (C, C)] * 3
        # Repeat.  Notice that the last turn is the 37th move, but we do not
        # defect.
        actions += [(C, D), (D, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        # Test for parity limit shortening.
        opponent_actions = [D, C] * 1000
        AsyncAlternator = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (C, C)] * 6
        # Defect on 37th move
        actions += [(D, D)]
        actions += [(C, C)]
        # This triggers the burned flag.  We should just Tit-for-Tat from here.
        actions += [(C, D)]
        actions += [(D, C), (C, D), (D, C), (C, D), (C, C)]
        # This is the seventh time we've hit the limit.  So do it once more.
        actions += [(C, D), (D, C), (C, D), (D, C), (C, D), (C, C)]
        # Now hit the limit sooner
        actions += [(C, D), (D, C), (C, D), (C, C)] * 5
        self.versus_test(AsyncAlternator, expected_actions=actions, attrs={"parity_limit": 3})

        # Use a Defector to test the 20-defect streak
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        # Now the two parity flags are used
        actions += [(C, D), (C, D)]
        # Repeat
        actions += [(D, D), (D, D), (D, D), (D, D), (C, D), (C, D)] * 2
        actions += [(D, D), (D, D)]
        # 20 D have passed (first isn't record)
        actions += [(D, D)] * 100
        # The defect streak will always be detected from here on, because it
        # doesn't reset.  This logic comes before parity streaks or the turn-
        # based logic.
        self.versus_test(axelrod.Defector(), expected_actions=actions, attrs={"recorded_defects": 119})

        # Detect random
        expected_actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (C, D), (D, D),
                   (D, C), (C, D), (D, C), (C, C), (C, D), (D, D), (D, C),
                   (C, D), (D, D), (D, C), (C, C), (C, D), (D, C), (C, D),
                   (D, D), (D, C), (C, D), (D, D), (D, D), (C, D), (D, C),
                   (C, C)]
        # Enter defect mode.
        expected_actions += [(D, C)]
        random.seed(10)
        player = self.player()
        match = axelrod.Match((player, axelrod.Random()), turns=len(expected_actions))
        # The history matrix will be [[0, 2], [5, 6], [3, 6], [4, 2]]
        actions = match.play()
        self.assertEqual(actions, expected_actions)  # Just to be consistant with the current test.
        self.assertAlmostEqual(player.calculate_chi_squared(len(expected_actions)), 2.395, places=4)

        # Come back out of defect mode
        opponent_actions = [D, C, D, C, D, D, D, C, D, C, C, D, D, C, D, D, C,
                            C, D, C, D, D, C, D, D, D, D, C, C, C]
        opponent_actions += [D] * 16
        Rand_Then_Def = axelrod.MockPlayer(actions=opponent_actions)
        actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (C, D), (D, D),
                   (D, C), (C, D), (D, C), (C, C), (C, D), (D, D), (D, C),
                   (C, D), (D, D), (D, C), (C, C), (C, D), (D, C), (C, D),
                   (D, D), (D, C), (C, D), (D, D), (D, D), (C, D), (D, C),
                   (C, C)]
        actions += [(D, C)]
        # Enter defect mode.
        actions += [(D, D)] * 14
        # Mutual defect for a while, then exit Defect mode with two coops
        actions += [(C, D)] * 2
        self.versus_test(Rand_Then_Def, expected_actions=actions, seed=10,
                        attrs={"mode": "Normal", "was_defective": True})
