"""Tests for the Memory Decay strategy"""

from inspect import getargspec
import axelrod
from axelrod.tests.strategies.test_player import TestPlayer

C, D = axelrod.Action.C, axelrod.Action.D

class TestMemoryDecay(TestPlayer):

    name = 'MemoryDecay'
    player = axelrod.MemoryDecay
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
        """Test TitForTat behavior in first 15 turns"""
        opponent = axelrod.MockPlayer(actions = [C, C])
        actions = [(C, C), (C, C), (C, C), (C, C)]
        self.versus_test(opponent, expected_actions = actions)

        opponent = axelrod.MockPlayer(actions = [D, D])
        actions = [(C, D), (D, D), (D, D), (D, D)]
        self.versus_test(opponent, expected_actions = actions)

t = TestMemoryDecay()
t.test_strategy()
