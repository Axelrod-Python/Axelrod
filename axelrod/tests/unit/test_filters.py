import unittest
from axelrod.strategies._filters import *
from hypothesis import given, example
from hypothesis.strategies import sampled_from, integers
import operator


class TestFilters(unittest.TestCase):

    @given(
        truthy=sampled_from([True, 'True', 'true', '1', 'Yes', 'yes']),
        falsy=sampled_from([False, 'False', 'false', '0', 'No', 'no'])
    )
    @example(truthy=True, falsy=False)
    def test_boolean_filter(self, truthy, falsy):

        class TestStrategy(object):
            classifier = {
                'stochastic': True,
                'inspects_source': False
            }

        self.assertTrue(
            passes_boolean_filter(TestStrategy, 'stochastic', truthy))
        self.assertFalse(
            passes_boolean_filter(TestStrategy, 'stochastic', falsy))
        self.assertTrue(
            passes_boolean_filter(TestStrategy, 'inspects_source', falsy))
        self.assertFalse(
            passes_boolean_filter(TestStrategy, 'inspects_source', truthy))


    @given(
        smaller=integers(min_value=0, max_value=9),
        larger=integers(min_value=11, max_value=100),
    )
    @example(smaller='2', larger='20')
    def test_operator_filter(self, smaller, larger):

        class TestStrategy(object):
            classifier = {
                'memory_depth': 10,
            }

        self.assertTrue(passes_operator_filter(
            TestStrategy, 'memory_depth', smaller, operator.ge))
        self.assertTrue(passes_operator_filter(
            TestStrategy, 'memory_depth', larger, operator.le))
        self.assertFalse(passes_operator_filter(
            TestStrategy, 'memory_depth', smaller, operator.le))
        self.assertFalse(passes_operator_filter(
            TestStrategy, 'memory_depth', larger, operator.ge))


    def test_list_filter(self):

        class TestStrategy(object):
            classifier = {
                'makes_use_of': ['game', 'length']
            }

        self.assertTrue(passes_in_list_filter(TestStrategy, 'makes_use_of', 'game'))
        self.assertTrue(passes_in_list_filter(TestStrategy, 'makes_use_of', 'length'))
        self.assertFalse(passes_in_list_filter(TestStrategy, 'makes_use_of', 'test'))
