import unittest
import warnings

import axelrod as axl
from axelrod.tests.property import strategy_lists
from hypothesis import example, given, settings
from hypothesis.strategies import data, integers, lists, sampled_from


class TestFiltersAgainstComprehensions(unittest.TestCase):
    """
    Test that the results of filtering strategies via a filterset dict
    match the results from using a list comprehension.
    """

    def setUp(self) -> None:
        # Ignore warnings about classifiers running on instances
        warnings.simplefilter("ignore", category=UserWarning)

    def tearDown(self) -> None:
        warnings.simplefilter("default", category=UserWarning)

    @settings(deadline=None)
    @given(
        strategies=strategy_lists(min_size=20, max_size=20),
        hypothesis_selector=data(),
    )
    def test_boolean_filtering(self, strategies, hypothesis_selector):

        classifier_list = [
            "stochastic",
            "long_run_time",
            "manipulates_state",
            "manipulates_source",
            "inspects_source",
        ]

        classifiers = hypothesis_selector.draw(
            lists(
                sampled_from(classifier_list),
                min_size=1,
                max_size=len(classifier_list),
                unique=True,
            )
        )

        comprehension, filterset = strategies, {}
        for classifier in classifiers:
            comprehension = set(
                filter(axl.Classifiers[classifier], strategies)
            ) & set(comprehension)
            filterset[classifier] = True
        filtered = set(
            axl.filtered_strategies(filterset, strategies=strategies)
        )
        self.assertEqual(comprehension, filtered)

    @given(
        min_memory_depth=integers(min_value=1, max_value=10),
        max_memory_depth=integers(min_value=1, max_value=10),
        memory_depth=integers(min_value=1, max_value=10),
        strategies=strategy_lists(min_size=20, max_size=20),
    )
    @example(
        min_memory_depth=float("inf"),
        max_memory_depth=float("inf"),
        memory_depth=float("inf"),
        strategies=axl.short_run_time_strategies,
    )
    @settings(max_examples=5, deadline=None)
    def test_memory_depth_filtering(
        self, min_memory_depth, max_memory_depth, memory_depth, strategies
    ):

        min_comprehension = set(
            [
                s
                for s in strategies
                if axl.Classifiers["memory_depth"](s) >= min_memory_depth
            ]
        )
        min_filterset = {"min_memory_depth": min_memory_depth}
        min_filtered = set(
            axl.filtered_strategies(min_filterset, strategies=strategies)
        )
        self.assertEqual(min_comprehension, min_filtered)

        max_comprehension = set(
            [
                s
                for s in strategies
                if axl.Classifiers["memory_depth"](s) <= max_memory_depth
            ]
        )
        max_filterset = {"max_memory_depth": max_memory_depth}
        max_filtered = set(
            axl.filtered_strategies(max_filterset, strategies=strategies)
        )
        self.assertEqual(max_comprehension, max_filtered)

        comprehension = set(
            [
                s
                for s in strategies
                if axl.Classifiers["memory_depth"](s) == memory_depth
            ]
        )
        filterset = {"memory_depth": memory_depth}
        filtered = set(
            axl.filtered_strategies(filterset, strategies=strategies)
        )
        self.assertEqual(comprehension, filtered)

    @given(strategies=strategy_lists(min_size=20, max_size=20))
    @settings(max_examples=5, deadline=None)
    def test_makes_use_of_filtering(self, strategies):
        """
        Test equivalent filtering using two approaches.
        """
        classifiers = [["game"], ["length"], ["game", "length"]]

        for classifier in classifiers:
            comprehension = set(
                [
                    s
                    for s in strategies
                    if set(classifier).issubset(
                        set(axl.Classifiers["makes_use_of"](s))
                    )
                ]
            )

            filterset = {"makes_use_of": classifier}
            filtered = set(
                axl.filtered_strategies(filterset, strategies=strategies)
            )

            self.assertEqual(
                comprehension, filtered, msg="classifier: {}".format(classifier)
            )
