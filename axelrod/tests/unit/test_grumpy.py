"""Tests for the grumpy strategy."""

import axelrod
from .test_player import TestPlayer, test_responses, TestOpponent

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGrumpy(TestPlayer):

    name = "Grumpy"
    player = axelrod.Grumpy
    expected_classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Starts by cooperating.
        self.first_play_test(C)
        # Starts by defecting if grumpy initially.
        self.responses_test(D, init_kwargs={"starting_state": "Grumpy"})
        # Tests that grumpy will play C until threshold is hit at which point it
        # will become grumpy. Player will then not become nice until lower nice
        # threshold is hit.

        self.responses_test(C, C + D * 3, C * 4,
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0},
                            attrs={"state": "Nice"})
        self.responses_test(D, C * 2 + D * 3, D * 5,
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0})
        self.responses_test(D, C * 2 + D * 6, D * 5 + C * 3,
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0})
        self.responses_test(C, C * 2 + D * 9, D * 5 + C * 6,
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0})

    def test_reset_method(self):
        P1 = axelrod.Grumpy(starting_state='Grumpy')
        P1.state = 'Nice'
        P1.reset()
        self.assertEqual(P1.state, 'Grumpy')
