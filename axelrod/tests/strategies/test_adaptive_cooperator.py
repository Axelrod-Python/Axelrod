import axelrod
from .test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D

class TestAdaptiveCooperator(TestPlayer):
    name = 'Adaptive Cooperator'
    player = axelrod.AdaptiveCooperator
    expected_classifier = {
       "memory_depth": 1,
        'stochastic': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy_cooperator(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.Cooperator(), expected_actions=actions)

    def test_strategy_defector(self):
        actions = [(C, D), (D, D), (D, D), (D, D), (D, D)]
        self.versus_test(axelrod.Defector(), expected_actions=actions)

    def test_strategy_alternator(self):
        actions = [(C, C), (C, D), (D, C), (D, D), (D, C)]
        self.versus_test(axelrod.Alternator(), expected_actions=actions)

    def test_strategy_tit4tat(self):
        actions = [(C, C), (C, C), (C, C), (C, C), (C, C)]
        self.versus_test(axelrod.TitForTat(), expected_actions=actions)
