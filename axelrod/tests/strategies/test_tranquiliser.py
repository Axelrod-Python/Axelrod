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
        
                             # Current score per turn:

        actions = [(C, C)]   # N/A
        
        actions += [(C, C)]  # 3
        
        actions += [(C, D)]  # 3

        actions += [(C, D)]  # 2

        actions += [(D, D)]  # 1.5   - Copied opponent's last move

        actions += [(D, C)]  # 1.4   - Copied opponent's last move

        actions += [(C, D)]  # 2

        actions += [(D, D)]  # 1.714 - Copied opponent's last move

        actions += [(D, D)]  # 1.625   - Copied opponent's last move

        actions += [(D, C)]  # 1.55   - Copied opponent's last move

        self.versus_test(opponent = opponent, expected_actions=actions)
        
    
    def score_between(self):

        # If score is between 1.75 and 2.25, may cooperate or defect
    
        opponent = axelrod.MockPlayer(actions = [D] * 8 + [C] * 5 + [D])

        actions = [(C, D)] + [(D, D)] * 7 + [(D, C)] + [(C, C)] * 4
    
        # average_score_per_turn = 1.875
    
        actions += ([(C, D)]) # <-- Random

        self.versus_test(opponent, expected_actions=actions, seed=1)

        
        
        opponent = axelrod.MockPlayer(actions = [D] * 8 + [C] * 4 + [D])

        actions = [(C, D)] + [(D, D)] * 7 + [(D, C)] + [(C, C)] * 3 
        
        # average_score_per_turn = 1.875
       
        actions += [(D, D)] # <-- Random
        
        self.versus_test(opponent, expected_actions=actions, seed=10, attrs = {"P" : .891025641025641})

    def score_greater(self):

        # If score is greater than 2.25 either cooperate or defect, if turn number <= 4; cooperate.
        
        opponent = axelrod.MockPlayer(actions = [C] * 5)
        
        actions = [(C, C)] * 4 + [(C, C)]
        
        self.versus_test(opponent, expected_actions = actions, seed = 1)
        


        opponent = axelrod.MockPlayer(actions = [C] * 5)

        actions = [(C, C)] * 4 + [(D, C)]

        self.versus_test(opponent, expected_actions = actions, seed = 70)



    def test_consecutive_defections(self):
        
        opponent = axelrod.Defector()

        actions = [(C, D)] + [(D, D)] * 19

        self.versus_test(opponent, expected_actions=actions, attrs={"consecutive_defections" : 19}) # Check

    def test_never_defects_twice(self):
        # Given score per turn is greater than 2.25, Tranquiliser will never defect twice in a row
        
        opponent = axelrod.MockPlayer(actions = [C] * 5)

        actions = [(C, C)] * 4 + [(D, C)]

        self.versus_test(opponent, expected_actions = actions, seed = 70, attrs={"FD" : 1})



        