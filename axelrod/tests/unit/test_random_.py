"""Test for the random strategy."""

import random
import unittest

from axelrod import random_choice, Actions

C, D = Actions.C, Actions.D

class TestRandom_(unittest.TestCase):

    def test_return_values(self):
        self.assertEqual(random_choice(1), C)
        self.assertEqual(random_choice(0), D)
        random.seed(1)
        self.assertEqual(random_choice(), C)
        random.seed(2)
        self.assertEqual(random_choice(), D)
