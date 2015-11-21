"""Test for the grumpy strategy."""

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
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_initial_nice_strategy(self):
        """
        Starts by cooperating
        """
        self.first_play_test(C)

    def test_initial_grumpy_strategy(self):
        """
        Starts by defecting if grumpy
        """
        P1 = axelrod.Grumpy(starting_state = 'Grumpy')
        P2 = TestOpponent()
        self.assertEqual(P1.strategy(P2), D)

    def test_strategy(self):
        """
        Tests that grumpy will play c until threshold is ht at which point it will become grumpy.
        Player will then not become nice until lower nice threshold is hit.
        """
        P1 = axelrod.Grumpy(grumpy_threshold = 3, nice_threshold=0)
        P2 = TestOpponent()
        test_responses(self, P1, P2, [C, D, D, D], [C, C, C, C], [C])

        P1 = axelrod.Grumpy(grumpy_threshold = 3, nice_threshold=0)
        P2 = TestOpponent()
        test_responses(self, P1, P2, [C, C, D, D, D], [D, D, D, D, D], [D])

        P1 = axelrod.Grumpy(grumpy_threshold = 3, nice_threshold=0)
        P2 = TestOpponent()
        test_responses(self, P1, P2, [C, C, D, D, D, D, D, D],
                       [D, D, D, D, D, C, C, C], [D])

        P1 = axelrod.Grumpy(grumpy_threshold = 3, nice_threshold=0)
        P2 = TestOpponent()
        test_responses(self, P1, P2, [C, C, D, D, D, D, D, D, D, D, D],
                       [D, D, D, D, D, C, C, C, C, C, C], [C])

    def test_reset_method(self):
        """
        tests the reset method
        """
        P1 = axelrod.Grumpy(starting_state = 'Grumpy')
        P1.history = [C, D, D, D]
        P1.state = 'Nice'
        P1.reset()
        self.assertEqual(P1.history, [])
        self.assertEqual(P1.state, 'Grumpy')
