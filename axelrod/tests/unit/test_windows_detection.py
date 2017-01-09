import unittest
import os
import axelrod


class TestWindowsDetection(unittest.TestCase):

    @unittest.skipIf(os.name == 'nt',
                     "Skip this test if on windows")
    def test_detection_on_not_windows(self):
        """Test when not on windows"""
        self.assertFalse(axelrod.on_windows)

    @unittest.skipIf(os.name != 'nt',
                     "Skip this test if not on windows")
    def test_detection_on_not_windows(self):
        """Test when on windows"""
        self.assertTrue(axelrod.on_windows)
