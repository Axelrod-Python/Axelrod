"""Test for the Worse and Worse strategy."""

import sys
import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestWorseAndWorse(TestPlayer):

    name = "Worse and worse"
    player = axelrod.WorseAndWorse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length']),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """
        Test that the strategy gives expected behaviour
        """
        axelrod.seed(1)
        opponent = axelrod.Cooperator()
        player = axelrod.WorseAndWorse()
        match = axelrod.Match((opponent, player), turns=5)
        self.assertEqual(match.play(), [('C', 'C'),
                                        ('C', 'D'),
                                        ('C', 'D'),
                                        ('C', 'D'),
                                        ('C', 'D')])

        # Test that behaviour does not depend on opponent
        opponent = axelrod.Defector()
        player = axelrod.WorseAndWorse()
        axelrod.seed(1)
        match = axelrod.Match((opponent, player), turns=5)
        self.assertEqual(match.play(), [('D', 'C'),
                                        ('D', 'D'),
                                        ('D', 'D'),
                                        ('D', 'D'),
                                        ('D', 'D')])

        # Test that behaviour changes when does not know length.
        axelrod.seed(1)
        match = axelrod.Match((opponent, player), turns=5,
                              match_attributes={'length': float('inf')})
        self.assertEqual(match.play(), [('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C')])
