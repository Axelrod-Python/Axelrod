import unittest
import axelrod

from numpy import mean
import tempfile

import matplotlib.pyplot
plt = matplotlib.pyplot


class TestPlot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = (
            axelrod.Alternator(), axelrod.TitForTat(), axelrod.Defector())
        cls.turns = 5
        cls.matches = {
            (0, 1): [axelrod.Match(
                (cls.players[0], cls.players[1]), turns=cls.turns)
                for _ in range(3)],
            (0, 2): [axelrod.Match(
                (cls.players[0], cls.players[2]), turns=cls.turns)
                for _ in range(3)],
            (1, 2): [axelrod.Match(
                (cls.players[1], cls.players[2]), turns=cls.turns)
                for _ in range(3)]
        }
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

        cls.test_result_set = axelrod.ResultSet(cls.players, cls.interactions,
                                                progress_bar=False)
        cls.expected_boxplot_dataset = [
            [(17 / 5 + 9 / 5) / 2 for _ in range(3)],
            [(13 / 5 + 4 / 5) / 2 for _ in range(3)],
            [3 / 2 for _ in range(3)]
        ]
        cls.expected_boxplot_xticks_locations = [1, 2, 3, 4]
        cls.expected_boxplot_xticks_labels = [
            'Defector', 'Tit For Tat', 'Alternator']

        cls.expected_lengthplot_dataset = [
            [cls.turns for _ in range(3)],
            [cls.turns for _ in range(3)],
            [cls.turns for _ in range(3)],
        ]

        cls.expected_payoff_dataset = [
            [0, mean(
                [9 / 5 for _ in range(3)]),
                mean([17 / 5 for _ in range(3)])],
            [mean(
                [4 / 5 for _ in range(3)]), 0,
                mean([13 / 5 for _ in range(3)])],
            [mean(
                [2 / 5 for _ in range(3)]),
                mean([13 / 5 for _ in range(3)]), 0]
        ]
        cls.expected_winplot_dataset = (
            [[2, 2, 2], [0, 0, 0], [0, 0, 0]],
            ['Defector', 'Tit For Tat', 'Alternator'])

    def test_default_cmap(self):
        cmap = axelrod.plot.default_cmap('0.0')
        self.assertEqual(cmap, 'YlGnBu')

        cmap = axelrod.plot.default_cmap('1.3alpha')
        self.assertEqual(cmap, 'YlGnBu')

        cmap = axelrod.plot.default_cmap('1.4.99')
        self.assertEqual(cmap, 'YlGnBu')

        cmap = axelrod.plot.default_cmap('1.4')
        self.assertEqual(cmap, 'YlGnBu')

        cmap = axelrod.plot.default_cmap()
        self.assertEqual(cmap, 'viridis')

        cmap = axelrod.plot.default_cmap('1.5')
        self.assertEqual(cmap, 'viridis')

        cmap = axelrod.plot.default_cmap('1.5beta')
        self.assertEqual(cmap, 'viridis')

        cmap = axelrod.plot.default_cmap('1.7')
        self.assertEqual(cmap, 'viridis')

        cmap = axelrod.plot.default_cmap('2.0')
        self.assertEqual(cmap, 'viridis')

    def test_init(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertEqual(plot.result_set, self.test_result_set)

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
        rs = axelrod.ResultSetFromFile(tmp_file.name, progress_bar=False)

        plot = axelrod.Plot(rs)
        self.assertEqual(plot.result_set, rs)

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
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.boxplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_boxplot_with_passed_axes(self):
        # Test that can plot on a given matplotlib axes
        fig, axarr = plt.subplots(2, 2)
        self.assertEqual(axarr[0, 1].get_ylim(), (0, 1))
        plot = axelrod.Plot(self.test_result_set)
        plot.boxplot(ax=axarr[0, 1])
        self.assertNotEqual(axarr[0, 1].get_ylim(), (0, 1))

        # Plot on another axes with a title
        plot.boxplot(title="dummy title", ax=axarr[1, 0])
        self.assertNotEqual(axarr[1, 0].get_ylim(), (0, 1))
        self.assertEqual(axarr[1, 0].get_title(), "dummy title")

    def test_boxplot_with_title(self):
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.boxplot(title="title")
        self.assertIsInstance(fig,
                              matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_winplot_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._winplot_dataset,
            self.expected_winplot_dataset)

    def test_winplot(self):
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.winplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_sdvplot(self):
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.sdvplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_lengthplot_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._winplot_dataset,
            self.expected_winplot_dataset)

    def test_lengthplot(self):
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.lengthplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_pdplot(self):
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.pdplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_payoff_dataset(self):
        plot = axelrod.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._payoff_dataset,
            self.expected_payoff_dataset)

    def test_payoff(self):
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.payoff()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_payoff_with_title(self):
        plot = axelrod.Plot(self.test_result_set)
        fig = plot.payoff(title="dummy title")
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_payoff_with_passed_axes(self):
        plot = axelrod.Plot(self.test_result_set)
        fig, axarr = plt.subplots(2, 2)
        self.assertEqual(axarr[0, 1].get_xlim(), (0, 1))

        plot.payoff(ax=axarr[0, 1])
        self.assertNotEqual(axarr[0, 1].get_xlim(), (0, 1))
        # Ensure color bar draw at same location as boxplot
        color_bar_bbox = fig.axes[-1].get_position().get_points()
        payoff_bbox_coord = fig.axes[1].get_position().get_points()
        self.assertEqual(color_bar_bbox[1, 1], payoff_bbox_coord[1, 1],
                         msg="Color bar is not in correct location.")

        # Plot on another axes with a title
        plot.payoff(title="dummy title", ax=axarr[1, 0])
        self.assertNotEqual(axarr[1, 0].get_xlim(), (0, 1))
        self.assertEqual(axarr[1, 0].get_xlabel(), "dummy title")

    def test_stackplot(self):
        eco = axelrod.Ecosystem(self.test_result_set)
        eco.reproduce(100)

        plot = axelrod.Plot(self.test_result_set)
        fig = plot.stackplot(eco)
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)
        fig = plot.stackplot(eco, title="dummy title")
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)
        fig = plot.stackplot(eco, logscale=False)
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_stackplot_with_passed_axes(self):
        # Test that can plot on a given matplotlib axes
        eco = axelrod.Ecosystem(self.test_result_set)
        eco.reproduce(100)
        plot = axelrod.Plot(self.test_result_set)

        fig, axarr = plt.subplots(2, 2)
        self.assertEqual(axarr[0, 1].get_xlim(), (0, 1))

        plot.stackplot(eco, ax=axarr[0, 1])
        self.assertNotEqual(axarr[0, 1].get_xlim(), (0, 1))

        # Plot on another axes with a title
        plot.stackplot(eco, title="dummy title", ax=axarr[1, 0])
        self.assertNotEqual(axarr[1, 0].get_xlim(), (0, 1))
        self.assertEqual(axarr[1, 0].get_title(), "dummy title")

    def test_all_plots(self):
        plot = axelrod.Plot(self.test_result_set)
        # Test that this method does not crash.
        self.assertIsNone(
            plot.save_all_plots(prefix="test_outputs/",
                                progress_bar=False))
        self.assertIsNone(
            plot.save_all_plots(prefix="test_outputs/",
                                title_prefix="A prefix",
                                progress_bar=True))
