"""Tests for the Graaskamp strategies."""

import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D

class TestMoreGraaskamp(TestPlayer):

    name = 'MoreGraaskamp'
    player = axelrod.MoreGraaskamp
    expected_classifier = {
        'memory_depth': 5,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False            
    }

    def test_against_cooperator(self):
        """
        Tests that the strategy plays as expected against a
        Cooperator
        """        

        # MoreGraaskamp should cooperate in the first round
        actions = [(C, C)]

        # MoreGraaskamp should play tit for tat until round 50
        actions += [(C, C)] * 49
        
        # MoreGraaskamp should defect in round 51
        actions += [(D, C)]

        # MoreGraaskamp should revert to tit for tat for rounds 52-56
        actions += [(C, C)] * 5
        
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

    def test_against_defector(self):
        """
        Tests that the strategy plays as expected against a
        Defector
        """        

        # MoreGraaskamp should cooperate in the first round
        actions = [(C, D)]

        # MoreGraaskamp should play tit for tat until round 50
        actions += [(D, D)] * 49

        # MoreGraaskamp should defect in round 51
        actions += [(D, D)]

        # MoreGraaskamp should revert to tit for tat for rounds 52-56
        actions += [(D, D)] * 5

        self.versus_test(axelrod.Defector(), expected_actions=actions)

    def test_against_alternator(self):
        """
        Tests that the strategy plays as expected against an
        Alternator
        """                

        # MoreGraaskamp should play tit for tat until round 50
        actions = [(C, C), (C, D)]
        actions += [(D, C), (C, D)] * 24

        # MoreGraaskamp should defect in round 51
        actions += [(D, C)]

        # MoreGraaskamp should revert to tit for tat for rounds 52-56
        actions += [(C, D), (D, C)] * 2 + [(C, D)]

        self.versus_test(axelrod.Alternator(), expected_actions=actions)        
        

    def test_mode_defect_randomly(self):
        """
        Tests that the strategy defects randomly every 5 to 15 after
        round 57 if none of the conditions for entering any of the other 
        modes are met.
        """

        # This is essentially testing against a cooperator
        actions = [(C, C)] * 50 + [(D, C)] + [(C, C)] * 49

        # With a fixed seed of 0, the strategy defects during these rounds
        actions[70] = (D, C)
        actions[83] = (D, C)
        actions[93] = (D, C)

        self.versus_test(axelrod.Cooperator(), expected_actions=actions, seed=0)

    def test_mode_tit_for_tat_late_alternator(self):
        """
        Tests that the strategy plays tit for tat starting with cooperate 
        f the opponent's score is greater than 135 in round 57 and moves 52 
        through 55 were [C, D, C, D]
        """

        # This opponent is a cooperator for rounds 1-51 and an alternator thereafter
        late_alternator_actions = [C] * 52 + [D, C] * 24
        late_alternator = axelrod.MockPlayer(actions=late_alternator_actions)

        # MoreGraaskamp should cooperate in the first round
        actions = [(C, C)]

        # MoreGraaskamp should play tit for tat until round 50
        actions += [(C, C)] * 49
        
        # MoreGraaskamp should defect in round 51
        actions += [(D, C)]

        # MoreGraaskamp should revert to tit for tat for rounds 52-56
        # Opponent plays trigger sequence [C, D, C, D] in rounds 52-55
        actions += [(C, C), (C, D), (D, C), (C, D), (D, C)]

        # MoreGraaskamp should play tit for tat starting with cooperate for the rest of the game
        actions += [(C, D), (D, C)] * 22

        self.versus_test(late_alternator, expected_actions=actions)

    def test_mode_tit_for_tat_late_defector(self):
        """
        Tests that the strategy plays tit for tat starting with cooperate 
        if the opponent's score is greater than 135 in round 57 and moves 52 
        through 55 were [D, D, D, D]
        """

        # This opponent is a cooperator for rounds 1-51 and a defector thereafter
        late_defector_actions = [C] * 51 + [D] * 49
        late_defector = axelrod.MockPlayer(actions=late_defector_actions)

        # MoreGraaskamp should cooperate in the first round
        actions = [(C, C)]

        # MoreGraaskamp should play tit for tat until round 50
        actions += [(C, C)] * 49
        
        # MoreGraaskamp should defect in round 51
        actions += [(D, C)]

        # MoreGraaskamp should revert to tit for tat for rounds 52-56
        # Opponent plays trigger sequence [D, D, D, D] in rounds 52-55
        actions += [(C, D), (D, D), (D, D), (D, D), (D, D)]

        # MoreGraaskamp should play tit for tat starting with cooperate for the rest of the game
        actions += [(C, D)] + [(D, D)] * 43

        self.versus_test(late_defector, expected_actions=actions)

    def test_mode_always_defect(self):
        """
        Tests that the strategy always defects after round 57
        when the opponent's score is less than 135
        """
        
        # This is essentially testing against a defector
        actions = [(C, D)] + [(D, D)] * 99

        self.versus_test(axelrod.Defector(), expected_actions=actions)

    def test_mode_cooperate_then_tit_for_tat(self):
        """
        Tests that if the opponent's score is greater than 135 at round 57 
        and moves 52 through 56 were [C, C, D, C, C], the strategy cooperates 
        until and including move 118, and plays tit for tat thereafter
        """
        
        opponent_actions = [C] * 51 + [C, C, D, C, C] + [D, C] * 47
        opponent = axelrod.MockPlayer(actions=opponent_actions)

        # MoreGraaskamp should cooperate in the first round
        actions = [(C, C)]

        # MoreGraaskamp should play tit for tat until round 50
        actions += [(C, C)] * 49
        
        # MoreGraaskamp should defect in round 51
        actions += [(D, C)]

        # MoreGraaskamp should revert to tit for tat for rounds 52-56
        # Opponent plays trigger sequence [C, C, D, C, C] in rounds 52-56
        actions += [(C, C), (C, C), (C, D), (D, C), (C, C)]

        # MoreGraaskamp should cooperate until and during round 118
        actions += [(C, D), (C, C)] * 31

        # MoreGraaskamp should play tit for tat for the rest of the game
        actions += [(C, D), (D, C)] * 16

        self.versus_test(opponent, expected_actions=actions)