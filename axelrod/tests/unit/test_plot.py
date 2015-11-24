import unittest
import axelrod

matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:
    matplotlib_installed = False


class TestPlot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        players = ('Player1', 'Player2', 'Player3')
        test_outcome = {
            'payoff': [
                [[0, 10, 21], [10, 0, 16], [16, 16, 0]],
                [[0, 10, 21], [8, 0, 20], [16, 16, 0]],
            ],
            'cooperation': []
        }
        cls.test_result_set = axelrod.ResultSet(players, 5, 2, test_outcome)
        cls.expected_boxplot_dataset = [[3.2, 3.2], [3.1, 3.1], [2.6, 2.8]]
        cls.expected_boxplot_xticks_locations = [1, 2, 3, 4]
        cls.expected_boxplot_xticks_labels = ['Player3', 'Player1', 'Player2']
        cls.expected_boxplot_title = ('Mean score per stage game over 5 turns'
                                      ' repeated 2 times (3 strategies)')
        cls.expected_payoff_dataset = [
            [0.0, 3.2, 3.2],
            [4.2, 0.0, 2.0],
            [3.6, 1.8, 0.0]]
        cls.expected_winplot_dataset = ([[1, 2], [0, 1], [0, 0]],
                                        ['Player1', 'Player2', 'Player3'])
        cls.expected_winplot_title = "Distributions of wins: 5 turns repeated 2 times (3 strategies)"

    def test_init(self):
        result_set = self.test_result_set
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(plot.result_set, self.test_result_set)
        self.assertEqual(matplotlib_installed, plot.matplotlib_installed)

    def test_boxplot_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._boxplot_dataset,
            self.expected_boxplot_dataset)

    def test_boxplot_xticks_locations(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(
            plot._boxplot_xticks_locations,
            self.expected_boxplot_xticks_locations)

    def test_boxplot_xticks_labels(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(
            plot._boxplot_xticks_labels,
            self.expected_boxplot_xticks_labels)

    def test_boxplot_title(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(plot._boxplot_title, self.expected_boxplot_title)

    def test_boxplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.boxplot(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_winplot_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._winplot_dataset,
            self.expected_winplot_dataset)

    def test_winplot_title(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(plot._winplot_title, self.expected_winplot_title)

    def test_winplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.winplot(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_payoff_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._payoff_dataset,
            self.expected_payoff_dataset)

    def test_payoff(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.payoff(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_ecosystem(self):
        if matplotlib_installed:
            eco = axelrod.Ecosystem(self.test_result_set)
            eco.reproduce(100)
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(
                plot.stackplot(eco), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')


if __name__ == '__main__':
    unittest.main()
