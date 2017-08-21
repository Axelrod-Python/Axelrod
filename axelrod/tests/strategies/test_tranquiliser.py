import axelrod
from Axelrod.axelrod.tests.strategies.test_player import TestPlayer
import unittest

C, D = axelrod.Action.C, axelrod.Action.D


class TestTranquiliser(TestPlayer):
    """
 Note that this test is referred to in the documentation as an example on
 writing tests.  If you modify the tests here please also modify the
 documentation.
 """

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
        self.assertEqual(player.ratioFD1, 5)
        self.assertEqual(player.ratioFD2, 0)
        self.assertEqual(player.ratioFD1_count, 0)
        self.assertEqual(player.ratioFD2_count, 0)
        self.assertEqual(player.score, None)


    def test_score_response(self):

        player = axelrod.Tranquiliser()        

        opponent = axelrod.Defector()

        actions = [(C, D)] + [(D, D)] * 20

        self.versus_test(opponent = opponent, expected_actions=actions)

        opponent = axelrod.MockPlayer([C] * 2 + [D] * 3 + [C] + [D] + [D] + [D] + [C] )
        
                             # Score

        actions = [(C, C)]   # N/A
        
        actions += [(C, C)]  # 3
        
        actions += [(C, D)]  # 3

        actions += [(C, D)]  # 2

        actions += [(D, D)]  # 1.5   - Copied

        actions += [(D, C)]  # 1.4   - Copied

        actions += [(C, D)]  # 2

        actions += [(D, D)]  # 1.714 - Copied

        actions += [(D, D)]  # 1.625   - Copied

        actions += [(D, C)]  # 1.55   - Copied

        self.versus_test(opponent = opponent, expected_actions=actions)
        
        
        # If score is between 1.75 and 2.25, probability of defection is always atleast than .25
    
        actions = [(C, D)]     

        actions += [(D, D)] * 7

        actions += [(D, C)]

        actions += [(C, C)] * 4
    
        actions += ([(C, D)])   # average_score_per_turn = 1.875, with probability of each action being .75 and .25 respectively

        self.versus_test(opponent = axelrod.MockPlayer(actions = [D] * 8 + [C] * 5 + [D]), expected_actions=actions, seed=1)


        

        actions = [(C, D)]     

        actions += [(D, D)] * 7

        actions += [(D, C)]

        actions += [(C, C)] * 3
    
        actions += ([(D, D)])    # average_score_per_turn = 1.875, with probability of each action being .75 and .25 respectively
        
        self.versus_test(opponent = axelrod.MockPlayer(actions = [D] * 8 + [C] * 4 + [D]), 
                        expected_actions=actions, seed=10, attrs = {"P" : .891025641025641})



        # If score is greater than 2.25 either cooperate or defect, if turn number <= 4; cooperate.
        
        opponent = axelrod.MockPlayer(actions = [C] * 5)
        
        actions = [(C, C)] * 4 + [(C, C)]
        
        self.versus_test(opponent, expected_actions = actions, seed = 1)

        opponent

        actions = [(C, C)] * 4 + [(D, C)]

        self.versus_test(opponent = axelrod.MockPlayer(actions = [C] * 5), expected_actions = actions, seed = 70)


    def test_consecutive_defections(self):
        
        player = axelrod.Tranquiliser()        
        
        actions = [(C, D)] + [(D, D)] * 19


        