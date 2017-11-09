"""Tests for the Memory Decay strategy"""

import axelrod as axe
from axelrod.tests.strategies.test_player import TestPlayer

C, D = axe.Action.C, axe.Action.D

class TestMemoryDecay(TestPlayer):

    name = 'MemoryDecay'
    player = axe.meta.MemoryDecay
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
        #Test TitForTat behavior in first 15 turns
        opponent = axe.Cooperator()
        actions = list([(C, C)]) * 15
        self.versus_test(opponent, expected_actions = actions)

        opponent = axe.Defector()
        actions = [(C, D)] + list([(D, D)]) * 14
        self.versus_test(opponent, expected_actions = actions)

        opponent = axe.Alternator()
        actions = [(C, C)] + [(C, D), (D, C)] * 7
        self.versus_test(opponent, expected_actions = actions)

        opponent_actions = [C, D, D, C, D, C, C, D, C, D, D, C, C, D, D]
        opponent = axe.MockPlayer(actions =opponent_actions)
        mem_actions = [C, C, D, D, C, D, C, C, D, C, D, D, C, C, D]
        actions = list(zip(mem_actions, opponent_actions))
        self.versus_test(opponent, expected_actions = actions)

        opponent = axe.Random()
        actions = [(C, D), (D, D), (D, C), (C, C), (C, D), (D, C)]
        self.versus_test(opponent, expected_actions = actions, seed = 0)

        #Test alternative starting strategies
        opponent = axe.Cooperator()
        actions = list([(D, C)]) * 15
        self.versus_test(opponent, expected_actions = actions,
                         init_kwargs = {'start_strategy' : 'Defector'})

        opponent = axe.Cooperator()
        actions = list([(C, C)]) * 15
        self.versus_test(opponent, expected_actions = actions,
                         init_kwargs = {'start_strategy' : 'Cooperator'})

        opponent = axe.Cooperator()
        actions = [(C, C)] + list([(D, C), (C, C)]) * 7
        self.versus_test(opponent, expected_actions = actions,
                         init_kwargs = {'start_strategy' : 'Alternator'})

        #Test net-cooperation-score (NCS) based decisions in subsequent turns
        opponent = axe.Cooperator()
        actions = [(C, C)] * 15 + [(C, C)]
        self.versus_test(opponent, expected_actions = actions, seed = 1,
                         init_kwargs = {'memory' : [D] * 5 + [C] * 10})

        opponent = axe.Cooperator()
        actions = [(C, C)] * 15 + [(C, C)]
        self.versus_test(opponent, expected_actions = actions, seed = 1,
                         init_kwargs = {'memory' : [D] * 4 + [C] * 11})

        opponent = axe.Defector()
        actions = [(C, D)] * 7 + [((D, D))]
        self.versus_test(opponent, expected_actions = actions, seed = 4,
                         init_kwargs = {'memory' : [C] * 12,
                                        'start_strategy' : 'Defector',
                                        'start_strategy_duration' : 0})
