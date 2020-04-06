import os
import pathlib
import unittest

from axelrod.load_data_ import axl_filename


class TestLoadData(unittest.TestCase):
    def test_axl_filename(self):
        path = pathlib.Path("axelrod/strategies/titfortat.py")
        actual_fn = axl_filename(path)

        # First go from "unit" up to "tests", then up to "axelrod"
        dirname = os.path.dirname(__file__)
        expected_fn = os.path.join(dirname, "../../strategies/titfortat.py")

        self.assertTrue(os.path.samefile(actual_fn, expected_fn))
