import unittest

import axelrod as axl


class TestNames(unittest.TestCase):
    def test_all_strategies_have_names(self):
        names = [s.name for s in axl.all_strategies if s.name != "Player"]
        self.assertEqual(len(names), len(axl.all_strategies))

    def test_all_names_are_unique(self):
        names = set(s.name for s in axl.all_strategies)
        self.assertEqual(len(names), len(axl.all_strategies))
