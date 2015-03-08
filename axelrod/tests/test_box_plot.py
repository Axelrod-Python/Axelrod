import unittest
import numpy
import axelrod

matplotlib_installed = True
try:
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib_installed = False


class TestBoxPlot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        players = ('Player1', 'Player2', 'Player3')
        results = [
            [[0, 0], [10, 10], [21, 21]],
            [[10, 8], [0, 0], [16, 20]],
            [[16, 16], [16, 16], [0, 0]]]
        cls.test_result_set = axelrod.ResultSet(players, 5, 2)
        cls.test_result_set.results = results
        cls.test_result_set.init_output()

        cls.expected_dataset = [[2.6, 2.8], [3.1, 3.1], [3.2, 3.2]]
        cls.expected_xticks_locations = [1, 2, 3, 4]
        cls.expected_xticks_labels = ['Player2', 'Player1', 'Player3']
        cls.expected_title = 'Mean score per stage game over 5 rounds repeated 2 times (3 strategies)'


    def test_init(self):
        bp = axelrod.BoxPlot(self.test_result_set)
        self.assertEquals(bp.result_set, self.test_result_set)

    def test_dataset(self):
        bp = axelrod.BoxPlot(self.test_result_set)
        self.assertTrue(numpy.allclose(bp.dataset(), self.expected_dataset))

    def test_xticks_locations(self):
        bp = axelrod.BoxPlot(self.test_result_set)
        self.assertEquals(bp.xticks_locations(), self.expected_xticks_locations)

    def test_xticks_labels(self):
        bp = axelrod.BoxPlot(self.test_result_set)
        self.assertEquals(bp.xticks_labels(), self.expected_xticks_labels)

    def test_title(self):
        bp = axelrod.BoxPlot(self.test_result_set)
        self.assertEquals(bp.title(), self.expected_title)

    def test_figure(self):
        if matplotlib_installed:
            bp = axelrod.BoxPlot(self.test_result_set)
            self.assertIsInstance(bp.figure(), plt.Figure)
        else:
            self.skipTest('matplotlib not installed')


if __name__ == '__main__':
    unittest.main()
