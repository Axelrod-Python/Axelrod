import unittest
from axelrod import all_strategies, filtered_strategies


class TestFiltersAgainstComprehensions(unittest.TestCase):

    def test_long_run_time(self):
        comprehension = [
            s for s in all_strategies if
            s().classifier['long_run_time']]
        filterset = {
            'long_run_time': True
        }
        filtered = filtered_strategies(filterset)
        self.assertEqual(comprehension, filtered)
