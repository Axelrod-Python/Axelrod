"""Tests for the Grumpy strategy."""

import axelrod
from .test_player import TestPlayer

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

        self.responses_test([C], [C, D, D, D], [C, C, C, C],
                            attrs={"state": "Nice"},
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0})
        self.responses_test([D], [C, C, D, D, D], [D, D, D, D, D],
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0})
        self.responses_test([D], [C, C, D, D, D, D, D, D],
                            [D, D, D, D, D, C, C, C],
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0})
        self.responses_test([C], [C, C, D, D, D, D, D, D, D, D, D],
                            [D, D, D, D, D, C, C, C, C, C, C],
                            init_kwargs={"grumpy_threshold": 3,
                                         "nice_threshold": 0})

    def test_reset_state(self):
        P1 = axelrod.Grumpy(starting_state='Grumpy')
        P1.state = 'Nice'
        P1.reset()
        self.assertEqual(P1.state, 'Grumpy')
