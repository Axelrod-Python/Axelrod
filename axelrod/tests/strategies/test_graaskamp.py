import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D


class TestGraaskamp(TestPlayer):
    """
    
    
    
    """

    name = "Graaskamp"
    player = axelrod.Graaskamp
    expected_classifier = {
        'memory_depth': 57,
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):

        # Play against opponents
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

        actions = [(C, C) * 50, (D, C), (C, C) * 5]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

        actions = [(C, D), (D, D) * 49, (D, D) * 6]
        self.versus_test(axelrod.Defector(), expected_actions=actions)
