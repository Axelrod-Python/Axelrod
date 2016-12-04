import unittest
from hypothesis import given, example, settings
from hypothesis.strategies import integers
from axelrod import all_strategies, filtered_strategies, MWERandom, seed


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

    @given(
        min_memory_depth=integers(min_value=1, max_value=10),
        max_memory_depth=integers(min_value=1, max_value=10),
        memory_depth=integers(min_value=1, max_value=10))
    @example(
        min_memory_depth=float('inf'),
        max_memory_depth=float('inf'),
        memory_depth=float('inf'))
    def test_memory_depth_filtering(self, min_memory_depth, max_memory_depth,
                                    memory_depth):

        min_comprehension = set([
            s for s in all_strategies if
            s.classifier['memory_depth'] >= min_memory_depth])
        min_filterset = {
            'min_memory_depth': min_memory_depth
        }
        min_filtered = set(filtered_strategies(min_filterset))
        self.assertEqual(min_comprehension, min_filtered)

        max_comprehension = set([
            s for s in all_strategies if
            s.classifier['memory_depth'] <= max_memory_depth])
        max_filterset = {
            'max_memory_depth': max_memory_depth
        }
        max_filtered = set(filtered_strategies(max_filterset))
        self.assertEqual(max_comprehension, max_filtered)

        comprehension = set([
            s for s in all_strategies if
            s.classifier['memory_depth'] == memory_depth])
        filterset = {
            'memory_depth': memory_depth
        }
        filtered = set(filtered_strategies(filterset))
        self.assertEqual(comprehension, filtered)

    @given(seed_=integers(min_value=0, max_value=4294967295))
    @settings(max_examples=10)
    def test_makes_use_of_filtering(self, seed_):
        """
        Test equivalent filtering using two approaches.

        This needs to be seeded as some players classification is random.
        """
        classifiers = [
            ['game'],
            ['length'],
            ['game', 'length']
        ]

        for classifier in classifiers:
            seed(seed_)
            comprehension = set([
                s for s in all_strategies if
                set(classifier).issubset(set(s().classifier['makes_use_of']))
            ])

            seed(seed_)
            filterset = {
                'makes_use_of': classifier
            }
            filtered = set(filtered_strategies(filterset))

            self.assertEqual(comprehension, filtered,
                             msg="classifier: {}".format(classifier))
