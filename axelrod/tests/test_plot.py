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
        test_payoffs_list = [
            [[0, 10, 21], [10, 0, 16], [16, 16, 0]],
            [[0, 10, 21], [8, 0, 20], [16, 16, 0]],
        ]
        cls.test_result_set = axelrod.ResultSet(players, 5, 2)
        cls.test_result_set.finalise(test_payoffs_list)

        cls.expected_boxplot_dataset = [[2.6, 2.8], [3.1, 3.1], [3.2, 3.2]]
        cls.expected_boxplot_xticks_locations = [1, 2, 3, 4]
        cls.expected_boxplot_xticks_labels = ['Player2', 'Player1', 'Player3']
        cls.expected_boxplot_title = ('Mean score per stage game over 5 rounds'
                                      ' repeated 2 times (3 strategies)')

        cls.expected_payoff_dataset = [
            [0.0, 1.8, 3.6],
            [2.0, 0.0, 4.2],
            [3.2, 3.2, 0.0]]

    def test_init(self):
        result_set = axelrod.ResultSet(('Player1', 'Player2', 'Player3'), 5, 2)
        self.assertRaises(AttributeError, axelrod.Plot, result_set)
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(plot.result_set, self.test_result_set)
        self.assertEqual(matplotlib_installed, plot.matplotlib_installed)

    def test_boxplot_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot.boxplot_dataset(),
            self.expected_boxplot_dataset)

    def test_boxplot_xticks_locations(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(
            plot.boxplot_xticks_locations(),
            self.expected_boxplot_xticks_locations)

    def test_boxplot_xticks_labels(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(
            plot.boxplot_xticks_labels(),
            self.expected_boxplot_xticks_labels)

    def test_boxplot_title(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(plot.boxplot_title(), self.expected_boxplot_title)

    def test_boxplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.boxplot(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_payoff_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot.payoff_dataset(),
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
            self.assertIsInstance(plot.stackplot(eco.population_sizes), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')


if __name__ == '__main__':
    unittest.main()
