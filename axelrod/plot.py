from distutils.version import LooseVersion

from .result_set import ResultSet
from numpy import arange, median, nan_to_num
import tqdm

from typing import List, Union

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

titleType = List[str]
namesType = List[str]
dataType = List[List[Union[int, float]]]


def default_cmap(version: str = "2.0") -> str:
    """Sets a default matplotlib colormap based on the version."""
    if LooseVersion(version) >= "1.5":
        return 'viridis'
    return 'YlGnBu'


class Plot(object):
    def __init__(self, result_set: ResultSet) -> None:
        self.result_set = result_set
        self.num_players = self.result_set.num_players
        self.players = self.result_set.players

    def _violinplot(
        self, data: dataType, names: namesType, title: titleType = None,
        ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """For making violinplots."""

        if ax is None:
            _, ax = plt.subplots()
        else:
            ax = ax

        figure = ax.get_figure()
        width = max(self.num_players / 3, 12)
        height = width / 2
        spacing = 4
        positions = spacing * arange(1, self.num_players + 1, 1)
        figure.set_size_inches(width, height)
        ax.violinplot(data, positions=positions, widths=spacing / 2,
                      showmedians=True, showextrema=False)
        ax.set_xticks(positions)
        ax.set_xticklabels(names, rotation=90)
        ax.set_xlim([0, spacing * (self.num_players + 1)])
        ax.tick_params(axis='both', which='both', labelsize=8)
        if title:
            ax.set_title(title)
        plt.tight_layout()
        return figure

    # Box and Violin plots for mean score, score differences, wins, and match
    # lengths

    @property
    def _boxplot_dataset(self):
        return [list(nan_to_num(self.result_set.normalised_scores[ir]))
                for ir in self.result_set.ranking]

    @property
    def _boxplot_xticks_locations(self):
        return list(range(1, len(self.result_set.ranked_names) + 2))

    @property
    def _boxplot_xticks_labels(self):
        return [str(n) for n in self.result_set.ranked_names]

    def boxplot(
        self, title: titleType = None, ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """For the specific mean score boxplot."""
        data = self._boxplot_dataset
        names = self._boxplot_xticks_labels
        figure = self._violinplot(data, names, title=title, ax=ax)
        return figure

    @property
    def _winplot_dataset(self):
        # Sort wins by median
        wins = self.result_set.wins
        medians = map(median, wins)
        medians = sorted(
            [(m, i) for (i, m) in enumerate(medians)], reverse=True)
        # Reorder and grab names
        wins = [wins[x[-1]] for x in medians]
        ranked_names = [str(self.players[x[-1]]) for x in medians]
        return wins, ranked_names

    def winplot(
        self, title: titleType = None, ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """Plots the distributions for the number of wins for each strategy."""

        data, names = self._winplot_dataset
        figure = self._violinplot(data, names, title=title, ax=ax)
        # Expand ylim a bit
        maximum = max(max(w) for w in data)
        plt.ylim(-0.5, 0.5 + maximum)
        return figure

    @property
    def _sd_ordering(self):
        return self.result_set.ranking

    @property
    def _sdv_plot_dataset(self):
        ordering = self._sd_ordering
        diffs = [[score_diff for opponent in player for score_diff in opponent]
                 for player in self.result_set.score_diffs]
        # Reorder and grab names
        diffs = [diffs[i] for i in ordering]
        ranked_names = [str(self.players[i]) for i in ordering]
        return diffs, ranked_names

    def sdvplot(
        self, title: titleType = None, ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """Score difference violin plots to visualize the distributions of how
        players attain their payoffs."""
        diffs, ranked_names = self._sdv_plot_dataset
        figure = self._violinplot(diffs, ranked_names, title=title, ax=ax)
        return figure

    @property
    def _lengthplot_dataset(self):
        match_lengths = self.result_set.match_lengths
        return [[length for rep in match_lengths
                 for length in rep[playeri]] for playeri in
                self.result_set.ranking]

    def lengthplot(
        self, title: titleType = None, ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """For the specific match length boxplot."""
        data = self._lengthplot_dataset
        names = self._boxplot_xticks_labels
        figure = self._violinplot(data, names, title=title, ax=ax)
        return figure

    @property
    def _payoff_dataset(self):
        pm = self.result_set.payoff_matrix
        return [[pm[r1][r2]
                 for r2 in self.result_set.ranking]
                for r1 in self.result_set.ranking]

    @property
    def _pdplot_dataset(self):
        # Order like the sdv_plot
        ordering = self._sd_ordering
        pdm = self.result_set.payoff_diffs_means
        # Reorder and grab names
        matrix = [[pdm[r1][r2] for r2 in ordering]
                  for r1 in ordering]
        players = self.result_set.players
        ranked_names = [str(players[i]) for i in ordering]
        return matrix, ranked_names

    def _payoff_heatmap(
        self, data: dataType, names: namesType, title: titleType = None,
        ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """Generic heatmap plot"""

        if ax is None:
            _, ax = plt.subplots()
        else:
            ax = ax

        figure = ax.get_figure()
        width = max(self.num_players / 4, 12)
        height = width
        figure.set_size_inches(width, height)
        matplotlib_version = matplotlib.__version__
        cmap = default_cmap(matplotlib_version)
        mat = ax.matshow(data, cmap=cmap)
        ax.set_xticks(range(self.result_set.num_players))
        ax.set_yticks(range(self.result_set.num_players))
        ax.set_xticklabels(names, rotation=90)
        ax.set_yticklabels(names)
        ax.tick_params(axis='both', which='both', labelsize=16)
        if title:
            ax.set_xlabel(title)
        figure.colorbar(mat, ax=ax)
        plt.tight_layout()
        return figure

    def pdplot(
        self, title: titleType = None, ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """Payoff difference heatmap to visualize the distributions of how
        players attain their payoffs."""
        matrix, names = self._pdplot_dataset
        return self._payoff_heatmap(matrix, names, title=title, ax=ax)

    def payoff(
        self, title: titleType = None, ax: matplotlib.axes.SubplotBase = None
    ) -> matplotlib.figure.Figure:
        """Payoff heatmap to visualize the distributions of how
        players attain their payoffs."""
        data = self._payoff_dataset
        names = self.result_set.ranked_names
        return self._payoff_heatmap(data, names, title=title, ax=ax)

    # Ecological Plot

    def stackplot(
        self, eco, title: titleType = None, logscale: bool = True,
        ax: matplotlib.axes.SubplotBase =None
    ) -> matplotlib.figure.Figure:

        populations = eco.population_sizes

        if ax is None:
            _, ax = plt.subplots()
        else:
            ax = ax

        figure = ax.get_figure()
        turns = range(len(populations))
        pops = [
            [populations[iturn][ir] for iturn in turns]
            for ir in self.result_set.ranking
        ]
        ax.stackplot(turns, *pops)

        ax.yaxis.tick_left()
        ax.yaxis.set_label_position("right")
        ax.yaxis.labelpad = 25.0

        ax.set_ylim([0.0, 1.0])
        ax.set_ylabel('Relative population size')
        ax.set_xlabel('Turn')
        if title is not None:
            ax.set_title(title)

        trans = transforms.blended_transform_factory(
            ax.transAxes, ax.transData)
        ticks = []
        for i, n in enumerate(self.result_set.ranked_names):
            x = -0.01
            y = (i + 0.5) * 1 / self.result_set.num_players
            ax.annotate(
                n, xy=(x, y), xycoords=trans, clip_on=False, va='center',
                ha='right', fontsize=5)
            ticks.append(y)
        ax.set_yticks(ticks)
        ax.tick_params(direction='out')
        ax.set_yticklabels([])

        if logscale:
            ax.set_xscale('log')

        plt.tight_layout()
        return figure

    def save_all_plots(
        self, prefix: str ="axelrod", title_prefix: str ="axelrod",
        filetype: str ="svg", progress_bar: bool = True
    ) -> None:
        """
        A method to save all plots to file.

        Parameters
        ----------

            prefix : str
                A prefix for the file name. This can include the directory.
                Default: axelrod.
            title_prefix : str
                A prefix for the title of the plots (appears on the graphic).
                Default: axelrod.
            filetype : str
                A string for the filetype to save files to: pdf, png, svg,
                etc...
            progress_bar : bool
                Whether or not to create a progress bar which will be updated
        """
        plots = [("boxplot", "Payoff"), ("payoff", "Payoff"),
                 ("winplot", "Wins"), ("sdvplot", "Payoff differences"),
                 ("pdplot", "Payoff differences"),
                 ("lengthplot", "Length of Matches")]

        if progress_bar:
            total = len(plots)  # Total number of plots
            pbar = tqdm.tqdm(total=total, desc="Obtaining plots")

        for method, name in plots:
            f = getattr(self, method)(title="{} - {}".format(title_prefix,
                                                             name))
            f.savefig("{}_{}.{}".format(prefix, method, filetype))
            plt.close(f)

            if progress_bar:
                pbar.update()
