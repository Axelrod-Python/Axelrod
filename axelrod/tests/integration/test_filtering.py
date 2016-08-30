import unittest
from axelrod import all_strategies, filtered_strategies


class TestFiltersAgainstComprehensions(unittest.TestCase):
    """
    Test that the results of filtering strategies via a filterset dict
    match the results from using a list comprehension.
    """

    def test_boolean_filtering(self):

        classifiers = [
            'stochastic',
            'long_run_time',
            'manipulates_state',
            'manipulates_source',
            'inspects_source']

        for classifier in classifiers:
            comprehension = set([
                s for s in all_strategies if
                s.classifier[classifier]])
            filterset = {
                classifier: True
            }
        filtered = set(filtered_strategies(filterset))
        self.assertEqual(comprehension, filtered)
