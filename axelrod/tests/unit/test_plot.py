import unittest
import axelrod

from numpy import mean
import tempfile

matplotlib_installed = True
try:
    import matplotlib.pyplot
except ImportError:
    matplotlib_installed = False


class TestPlot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = (axelrod.Alternator(), axelrod.TitForTat(), axelrod.Defector())
        cls.turns = 5
        cls.matches = {
                        (0, 1): [axelrod.Match((cls.players[0], cls.players[1]),
                        turns=cls.turns) for _ in range(3)],
                        (0, 2): [axelrod.Match((cls.players[0], cls.players[2]),
                        turns=cls.turns) for _ in range(3)],
                        (1, 2): [axelrod.Match((cls.players[1], cls.players[2]),
                        turns=cls.turns) for _ in range(3)]}
                        # This would not actually be a round robin tournament
                        # (no cloned matches)

        cls.interactions = {}
        for index_pair, matches in cls.matches.items():
            for match in matches:
                match.play()
                try:
                    cls.interactions[index_pair].append(match.result)
                except KeyError:
                    cls.interactions[index_pair] = [match.result]

        cls.test_result_set = axelrod.ResultSet(cls.players, cls.interactions)
        cls.expected_boxplot_dataset = [
               [(17.0 / 5 + 9.0 / 5) / 2 for _ in range(3)],
               [(13.0 / 5 + 4.0 / 5) / 2 for _ in range(3)],
               [3.0 / 2 for _ in range(3)]
               ]
        cls.expected_boxplot_xticks_locations = [1, 2, 3, 4]
        cls.expected_boxplot_xticks_labels = ['Defector', 'Tit For Tat', 'Alternator']

        cls.expected_lengthplot_dataset = [
               [cls.turns for _ in range(3)],
               [cls.turns for _ in range(3)],
               [cls.turns for _ in range(3)],
               ]

        cls.expected_payoff_dataset = [
            [0, mean([9/5.0 for _ in range(3)]), mean([17/5.0 for _ in range(3)])],
            [mean([4/5.0 for _ in range(3)]), 0, mean([13/5.0 for _ in range(3)])],
            [mean([2/5.0 for _ in range(3)]), mean([13/5.0 for _ in range(3)]), 0]
        ]
        cls.expected_winplot_dataset = ([[2, 2, 2], [0, 0, 0], [0, 0, 0]],
                                        ['Defector', 'Tit For Tat', 'Alternator'])

    def test_init(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(plot.result_set, self.test_result_set)
        self.assertEqual(matplotlib_installed, plot.matplotlib_installed)

    def test_init_from_resulsetfromfile(self):
        tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tournament = axelrod.Tournament(
            players=[axelrod.Cooperator(),
                     axelrod.TitForTat(),
                     axelrod.Defector()],
            turns=2,
            repetitions=2)
        tournament.play(filename=tmp_file.name, progress_bar=False)
        tmp_file.close()
        rs = axelrod.ResultSetFromFile(tmp_file.name)

        plot = axelrod.Plot(rs)
        self.assertEqual(plot.result_set, rs)
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

    def test_boxplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.boxplot(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_boxplot_with_title(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.boxplot(title="title"),
                                  matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_winplot_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._winplot_dataset,
            self.expected_winplot_dataset)

    def test_winplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.winplot(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_sdvplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.sdvplot(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_lengthplot_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._winplot_dataset,
            self.expected_winplot_dataset)

    def test_lengthplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.lengthplot(), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_pdplot(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.pdplot(), matplotlib.pyplot.Figure)
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

    def test_payoff_with_title(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(plot.payoff(title="dummy title"),
                                  matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_ecosystem(self):
        if matplotlib_installed:
            eco = axelrod.Ecosystem(self.test_result_set)
            eco.reproduce(100)
            plot = axelrod.Plot(self.test_result_set)
            self.assertIsInstance(
                plot.stackplot(eco), matplotlib.pyplot.Figure)
            self.assertIsInstance(
                plot.stackplot(eco, title="dummy title"),
                matplotlib.pyplot.Figure)
            self.assertIsInstance(
                plot.stackplot(eco, logscale=False), matplotlib.pyplot.Figure)
        else:
            self.skipTest('matplotlib not installed')

    def test_all_plots(self):
        if matplotlib_installed:
            plot = axelrod.Plot(self.test_result_set)
            # Test that this method does not crash.
            self.assertIsNone(
                plot.save_all_plots(prefix="test_outputs/",
                                    progress_bar=False))
            self.assertIsNone(
                plot.save_all_plots(prefix="test_outputs/",
                                    title_prefix="A prefix",
                                    progress_bar=False))
        else:
            self.skipTest('matplotlib not installed')


if __name__ == '__main__':
    unittest.main()
