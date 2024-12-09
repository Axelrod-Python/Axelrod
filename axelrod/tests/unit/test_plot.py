import pathlib
import tempfile
import unittest

import matplotlib
import matplotlib.pyplot as plt
from numpy import mean

import axelrod as axl
from axelrod.load_data_ import axl_filename


class TestPlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = pathlib.Path("test_outputs/test_results.csv")
        cls.filename = axl_filename(path)

        cls.players = [axl.Alternator(), axl.TitForTat(), axl.Defector()]
        cls.repetitions = 3
        cls.turns = 5

        cls.test_result_set = axl.ResultSet(
            cls.filename, cls.players, cls.repetitions, progress_bar=False
        )

        cls.test_result_set = axl.ResultSet(
            cls.filename, cls.players, cls.repetitions, progress_bar=False
        )
        cls.expected_boxplot_dataset = [
            [(17 / 5 + 9 / 5) / 2 for _ in range(3)],
            [(13 / 5 + 4 / 5) / 2 for _ in range(3)],
            [3 / 2 for _ in range(3)],
        ]
        cls.expected_boxplot_xticks_locations = [1, 2, 3, 4]
        cls.expected_boxplot_xticks_labels = [
            "Defector",
            "Tit For Tat",
            "Alternator",
        ]

        cls.expected_lengthplot_dataset = [
            [cls.turns for _ in range(3)],
            [cls.turns for _ in range(3)],
            [cls.turns for _ in range(3)],
        ]

        cls.expected_payoff_dataset = [
            [
                0,
                mean([9 / 5 for _ in range(3)]),
                mean([17 / 5 for _ in range(3)]),
            ],
            [
                mean([4 / 5 for _ in range(3)]),
                0,
                mean([13 / 5 for _ in range(3)]),
            ],
            [
                mean([2 / 5 for _ in range(3)]),
                mean([13 / 5 for _ in range(3)]),
                0,
            ],
        ]
        cls.expected_winplot_dataset = (
            [[2, 2, 2], [0, 0, 0], [0, 0, 0]],
            ["Defector", "Tit For Tat", "Alternator"],
        )

        cls.expected_sdvplot_dataset = (
            [
                [3, 3, 3, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, -1, -1, -1],
                [0, 0, 0, 0, 0, 0, -3, -3, -3],
            ],
            ["Defector", "Tit For Tat", "Alternator"],
        )

    def test_init(self):
        plot = axl.Plot(self.test_result_set)
        self.assertEqual(plot.result_set, self.test_result_set)

    def test_init_from_resulsetfromfile(self):
        tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        players = [axl.Cooperator(), axl.TitForTat(), axl.Defector()]
        tournament = axl.Tournament(players=players, turns=2, repetitions=2)
        tournament.play(filename=tmp_file.name, progress_bar=False)
        tmp_file.close()
        rs = axl.ResultSet(tmp_file.name, players, 2, progress_bar=False)

        plot = axl.Plot(rs)
        self.assertEqual(plot.result_set, rs)

    def test_boxplot_dataset(self):
        plot = axl.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._boxplot_dataset, self.expected_boxplot_dataset
        )

    def test_boxplot_xticks_locations(self):
        plot = axl.Plot(self.test_result_set)
        self.assertEqual(
            plot._boxplot_xticks_locations,
            self.expected_boxplot_xticks_locations,
        )

    def test_boxplot_xticks_labels(self):
        plot = axl.Plot(self.test_result_set)
        self.assertEqual(
            plot._boxplot_xticks_labels, self.expected_boxplot_xticks_labels
        )

    def test_boxplot(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.boxplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_boxplot_with_passed_axes(self):
        # Test that can plot on a given matplotlib axes
        fig, axarr = plt.subplots(2, 2)
        self.assertEqual(axarr[0, 1].get_ylim(), (0, 1))
        plot = axl.Plot(self.test_result_set)
        plot.boxplot(ax=axarr[0, 1])
        self.assertNotEqual(axarr[0, 1].get_ylim(), (0, 1))

        # Plot on another axes with a title
        plot.boxplot(title="dummy title", ax=axarr[1, 0])
        self.assertNotEqual(axarr[1, 0].get_ylim(), (0, 1))
        self.assertEqual(axarr[1, 0].get_title(), "dummy title")

    def test_boxplot_with_title(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.boxplot(title="title")
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_winplot_dataset(self):
        plot = axl.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._winplot_dataset, self.expected_winplot_dataset
        )

    def test_winplot(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.winplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_sdvplot_dataset(self):
        plot = axl.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._sdv_plot_dataset, self.expected_sdvplot_dataset
        )

    def test_sdvplot(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.sdvplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_lengthplot_dataset(self):
        plot = axl.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._winplot_dataset, self.expected_winplot_dataset
        )

    def test_lengthplot(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.lengthplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_pdplot(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.pdplot()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_payoff_dataset(self):
        plot = axl.Plot(self.test_result_set)
        self.assertSequenceEqual(
            plot._payoff_dataset, self.expected_payoff_dataset
        )

    def test_payoff(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.payoff()
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_payoff_with_title(self):
        plot = axl.Plot(self.test_result_set)
        fig = plot.payoff(title="dummy title")
        self.assertIsInstance(fig, matplotlib.pyplot.Figure)
        plt.close(fig)

    def test_payoff_with_passed_axes(self):
        plot = axl.Plot(self.test_result_set)
        fig, axarr = plt.subplots(2, 2)
        self.assertEqual(axarr[0, 1].get_xlim(), (0, 1))

        plot.payoff(ax=axarr[0, 1])
        self.assertNotEqual(axarr[0, 1].get_xlim(), (0, 1))

        # Plot on another axes with a title
        plot.payoff(title="dummy title", ax=axarr[1, 0])
        self.assertNotEqual(axarr[1, 0].get_xlim(), (0, 1))
        self.assertEqual(axarr[1, 0].get_xlabel(), "dummy title")
        plt.close(fig)

    def test_stackplot(self):
        eco = axl.Ecosystem(self.test_result_set)
        eco.reproduce(100)

        plot = axl.Plot(self.test_result_set)
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
        eco = axl.Ecosystem(self.test_result_set)
        eco.reproduce(100)
        plot = axl.Plot(self.test_result_set)

        fig, axarr = plt.subplots(2, 2)
        self.assertEqual(axarr[0, 1].get_xlim(), (0, 1))

        plot.stackplot(eco, ax=axarr[0, 1])
        self.assertNotEqual(axarr[0, 1].get_xlim(), (0, 1))

        # Plot on another axes with a title
        plot.stackplot(eco, title="dummy title", ax=axarr[1, 0])
        self.assertNotEqual(axarr[1, 0].get_xlim(), (0, 1))
        self.assertEqual(axarr[1, 0].get_title(), "dummy title")
        plt.close(fig)

    def test_all_plots(self):
        plot = axl.Plot(self.test_result_set)
        # Test that this method does not crash.
        self.assertIsNone(
            plot.save_all_plots(prefix="test_outputs/", progress_bar=False)
        )
        self.assertIsNone(
            plot.save_all_plots(
                prefix="test_outputs/",
                title_prefix="A prefix",
                progress_bar=True,
            )
        )

    def test_figure_generation_failure_violinplot(self):
        plot = axl.Plot(self.test_result_set)
        with self.assertRaises(RuntimeError):
            plot._violinplot(
                [0, 0, 0], ["a", "b", "c"], get_figure=lambda _: None
            )

    def test_figure_generation_failure_payoff_heatmap(self):
        plot = axl.Plot(self.test_result_set)
        with self.assertRaises(RuntimeError):
            plot._payoff_heatmap(
                [0, 0, 0], ["a", "b", "c"], get_figure=lambda _: None
            )

    def test_figure_generation_failure_stackplot(self):
        plot = axl.Plot(self.test_result_set)
        eco = axl.Ecosystem(self.test_result_set)
        with self.assertRaises(RuntimeError):
            plot.stackplot(eco, get_figure=lambda _: None)
