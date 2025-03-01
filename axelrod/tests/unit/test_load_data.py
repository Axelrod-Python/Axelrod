import os
import pathlib
import unittest
from unittest.mock import patch

import torch

from axelrod.load_data_ import (
    axl_filename,
    load_attention_model_weights,
    load_file,
)


class TestLoadData(unittest.TestCase):
    def test_axl_filename(self):
        path = pathlib.Path("axelrod/strategies/titfortat.py")
        actual_fn = axl_filename(path)

        # First go from "unit" up to "tests", then up to "axelrod"
        dirname = os.path.dirname(__file__)
        expected_fn = os.path.join(dirname, "../../strategies/titfortat.py")

        self.assertTrue(os.path.samefile(actual_fn, expected_fn))

    def test_raise_error_if_file_empty(self):
        path = pathlib.Path("not/a/file.py")
        with self.assertRaises(FileNotFoundError):
            load_file(path, ".")

    def test_raise_error_if_something(self):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, "../../strategies/titfortat.py")
        bad_loader = lambda _, __: None
        with self.assertRaises(FileNotFoundError):
            load_file(path, ".", bad_loader)

    def test_load_attention_model_weights(self):
        """Test that the load_attention_model_weights function works correctly."""
        # Create a mock object to return
        mock_weights = {
            "layer1": torch.tensor([1.0, 2.0]),
            "layer2": torch.tensor([3.0, 4.0]),
        }

        # Patch torch.load to return our mock weights
        with patch(
            "axelrod.load_data_.torch.load", return_value=mock_weights
        ) as mock_load:
            # Call our function
            result = load_attention_model_weights()

            # Check that torch.load was called once
            mock_load.assert_called_once()

            # Check that the path passed to torch.load contains the expected components
            args, kwargs = mock_load.call_args
            self.assertIn("model_attention.pth", args[0])
            self.assertEqual(kwargs["map_location"], torch.device("cpu"))

            # Check that the function returned our mock weights
            self.assertEqual(result, mock_weights)
