"""Test for the Worse and Worse strategies."""

import axelrod

from .test_player import TestPlayer

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestWorseAndWorse(TestPlayer):

    name = "Worse and Worse"
    player = axelrod.WorseAndWorse
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
        """
        Test that the strategy gives expected behaviour
        """

        axelrod.seed(8)
        opponent = axelrod.Cooperator()
        player = axelrod.WorseAndWorse()
        match = axelrod.Match((opponent, player), turns=10)
        self.assertEqual(match.play(), [('C', 'C'),
                                        ('C', 'C'),
                                        ('C', 'C'),
                                        ('C', 'C'),
                                        ('C', 'C'),
                                        ('C', 'C'),
                                        ('C', 'D'),
                                        ('C', 'C'),
                                        ('C', 'C'),
                                        ('C', 'C')])

        # Test that behaviour does not depend on opponent
        opponent = axelrod.Defector()
        player = axelrod.WorseAndWorse()
        axelrod.seed(8)
        match = axelrod.Match((opponent, player), turns=10)
        self.assertEqual(match.play(), [('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'D'),
                                        ('D', 'C'),
                                        ('D', 'C'),
                                        ('D', 'C')])


class TestWorseAndWorseRandom(TestPlayer):

    name = "Knowledgeable Worse and Worse"
    player = axelrod.KnowledgeableWorseAndWorse
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
        player = axelrod.KnowledgeableWorseAndWorse()
        match = axelrod.Match((opponent, player), turns=5)
        self.assertEqual(match.play(), [('C', 'C'),
                                        ('C', 'D'),
                                        ('C', 'D'),
                                        ('C', 'D'),
                                        ('C', 'D')])

        # Test that behaviour does not depend on opponent
        opponent = axelrod.Defector()
        player = axelrod.KnowledgeableWorseAndWorse()
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


class TestWorseAndWorse2(TestPlayer):

    name = "Worse and Worse 2"
    player = axelrod.WorseAndWorse2
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
        """
        Test that the strategy gives expected behaviour
        """

        # Test that first move is C
        self.responses_test([], [], [C])

        # Test that given a history, next move matches opponent (round <= 20)
        self.responses_test([C], [C], [C])
        self.responses_test([C, C], [C, D], [D])
        self.responses_test([C] * 19, [C] * 19, [C])
        self.responses_test([C] * 19, [C] * 18 + [D], [D])

        # Test that after round 20, strategy follows stochastic behaviour given
        # a seed
        self.responses_test([C] * 20, [C] * 20, [C, D, C, C, C, C, D, C, C, C], random_seed=8)
        self.responses_test([C] * 20, [C] * 20, [D, D, C, C, D, C, C, C, C, C], random_seed=2)
