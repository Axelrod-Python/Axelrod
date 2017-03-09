"""Tests for the WorseAndWorse strategies."""

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
        """Test that the strategy gives expected behaviour."""
        self.first_play_test(C)
        self.responses_test([C] * 6 + [D] + [C] * 3, seed=8)
        self.responses_test([C] * 4 + [D] + [C] * 3, [C, C], [D, D], seed=8)


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
        """Test that the strategy gives expected behaviour."""
        self.first_play_test(C)
        # self.responses_test([C] + [D] * 4, seed=1)
        # self.responses_test([C] * 4 + [D] + [C] * 3, [C, C],
        #                     [D, D], seed=1)

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
        """Test that the strategy gives expected behaviour."""
        # Test that first move is C
        self.first_play_test('C')
        # Test that given a history, next move matches opponent (round <= 20)
        self.responses_test([C], [C], [C])
        self.responses_test([D], [C, C], [C, D])
        self.responses_test([C], [C] * 19, [C] * 19)
        self.responses_test([D], [C] * 19, [C] * 18 + [D])
        # Test that after round 20, strategy follows stochastic behaviour given
        # a seed
        self.responses_test([C, D, C, C, C, C, D, C, C, C], [C] * 20, [C] * 20,
                            seed=8)
        self.responses_test([D, D, C, C, D, C, C, C, C, C], [C] * 20, [C] * 20,
                            seed=2)


class TestWorseAndWorse3(TestPlayer):

    name = "Worse and Worse 3"
    player = axelrod.WorseAndWorse3
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
        """Test that the strategy gives expected behaviour."""
        # Test that first move is C
        self.first_play_test(C)
        # Test that if opponent only defects, strategy also defects
        self.responses_test([D], [D] * 5, [D] * 5)
        # Test that if opponent only cooperates, strategy also cooperates
        self.responses_test([C], [C] * 5, [C] * 5)
        # Test that given a non 0/1 probability of defecting, strategy follows
        # stochastic behaviour, given a seed
        self.responses_test([D, C, C, D, C, C, C, C, C, C], [C] * 5,
                            [C, D, C, D, C], seed=8)
        self.responses_test([D, D, D, C, C, D, D, D, C, C], [C] * 5, [D] * 5,
                            seed=2)
