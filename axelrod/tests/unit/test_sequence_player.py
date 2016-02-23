"""Test for the Thue-Morse strategies."""
import unittest
import itertools

import axelrod
from .test_player import TestPlayer
from axelrod.strategies.sequence_player import recursive_thue_morse


C, D = axelrod.Actions.C, axelrod.Actions.D

def alternator_generator(start=0):
    """A generator for alternator."""
    for n in itertools.count(start):
        yield n%2


class TestThueMoreGenerator(unittest.TestCase):
    def test_sequence(self):
        expected = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
        for i, e in enumerate(expected):
            self.assertEqual(recursive_thue_morse(i), e)


class TestAlternatorSequencePlayer(axelrod.SequencePlayer):
    """
    A test player who is the same as Alternator.
    """

    name = 'TestAlternatorSequencePlayer'
    classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    @axelrod.init_args
    def __init__(self):
        axelrod.SequencePlayer.__init__(self, alternator_generator, (0,))



class TestSequencePlayer(TestPlayer):
    
    name = 'TestAlternatorSequencePlayer'
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    player = TestAlternatorSequencePlayer

    def test_strategy(self):
        """Test that strategy always picks D first."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):
        self.responses_test([], [], [D, C, D, C, D, C, D, C, D, C, D, C, D, C,
                                     D, C])
        self.responses_test([C], [C], [C, D, C, D, C, D, C, D, C, D, C, D, C,
                                     D, C])
        self.responses_test([D], [D], [C, D, C, D, C, D, C, D, C, D, C, D, C,
                                     D, C])
        self.responses_test([C, C, C, D], [C, C, C, D], [D, C, D, C, D, C, D, C,
                                                         D, C, D, C])




class TestThueMorse(TestPlayer):

    name = 'ThueMorse'
    player = axelrod.ThueMorse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that strategy always picks D first."""
        self.first_play_test(D)

    def test_effect_of_strategy(self):
        self.markov_test([C, C, C, C])
        self.responses_test([], [], [D, C, C, D, C, D, D, C, C, D, D, C, D, C,
                                     C, D])
        self.responses_test([C], [C], [C, C, D, C, D, D, C, C, D, D, C, D, C, C,
                                       D])
        self.responses_test([D], [D], [C, C, D, C, D, D, C, C, D, D, C, D, C, C,
                                       D])
        self.responses_test([C, C, C, D], [C, C, C, D], [C, D, D, C, C, D, D, C,
                                                         D, C, C, D])


class TestThueMorseInverse(TestPlayer):

    name = 'ThueMorseInverse'
    player = axelrod.ThueMorseInverse
    expected_classifier = {
        'memory_depth': float('inf'),
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        """Test that strategy always picks C first."""
        self.first_play_test(C)
        self.first_play_test(C)

    def test_effect_of_strategy(self):
        self.markov_test([D, D, D, D])
        self.responses_test([], [], [C, D, D, C, D, C, C, D, D, C, C, D, C, D,
                                     D, C])
        self.responses_test([C], [C], [D, D, C, D, C, C, D, D, C, C, D, C, D, D,
                                       C])
        self.responses_test([D], [D], [D, D, C, D, C, C, D, D, C, C, D, C, D, D,
                                       C])
        self.responses_test([C, C, C, D], [C, C, C, D], [D, C, C, D, D, C, C, D,
                                                         C, D, D, C])
