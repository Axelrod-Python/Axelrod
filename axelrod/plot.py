
from numpy.linalg import LinAlgError
from numpy import arange, mean, median
from warnings import warn

matplotlib_installed = True
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.transforms as transforms
    from mpl_toolkits.axes_grid1 import make_axes_locatable
except ImportError:
    matplotlib_installed = False


def default_cmap():
    """Sets a default matplotlib colormap based on the version."""
    s = matplotlib.__version__.split('.')
    if int(s[0]) >= 1 and int(s[1]) >= 5:
        return "viridis"
    else:
        return 'YlGnBu'


class Plot(object):

    def __init__(self, result_set):
        self.result_set = result_set
        self.matplotlib_installed = matplotlib_installed

    ## Abstract Box and Violin plots

    def _boxplot(self, data, names, title=None):
        """For making boxplots."""
        if not self.matplotlib_installed:
            return None
        nplayers = self.result_set.nplayers
        width = max(nplayers / 3, 12)
        height = width / 2
        figure = plt.figure(figsize=(width, height))
        plt.boxplot(data)
        plt.xticks(self._boxplot_xticks_locations, names, rotation=90)
        plt.tick_params(axis='both', which='both', labelsize=8)
        if title:
            plt.title(title)
        return figure

    def _violinplot(self, data, names, title=None):
        """For making violinplots."""
        if not self.matplotlib_installed:
            return None
        nplayers = self.result_set.nplayers
        width = max(nplayers / 3, 12)
        height = width / 2
        figure = plt.figure(figsize=(width, height))
        spacing = 4
        positions = spacing * arange(1, nplayers + 1, 1)
        plt.violinplot(data, positions=positions, widths=spacing/2,
                       showmedians=True, showextrema=False)
        plt.xticks(positions, names, rotation=90)
        plt.xlim(0, spacing * (nplayers + 1))
        plt.tick_params(axis='both', which='both', labelsize=8)
        if title:
            plt.title(title)
        return figure

    ## Box and Violin plots for mean score, score diferrences, and wins

    @property
    def _boxplot_dataset(self):
        return [self.result_set.normalised_scores[ir] for ir in self.result_set.ranking]

    @property
    def _boxplot_xticks_locations(self):
        return list(range(1, len(self.result_set.ranked_names) + 2))

    @property
    def _boxplot_xticks_labels(self):
        return [str(n) for n in self.result_set.ranked_names]

    @property
    def _boxplot_title(self):
        return ("Mean score per stage game over {} "
                "turns repeated {} times ({} strategies)").format(
            self.result_set.turns,
            self.result_set.repetitions,
            len(self.result_set.ranking))

    def boxplot(self):
        """For the specific mean score boxplot."""
        data = self._boxplot_dataset
        names = self._boxplot_xticks_labels
        title = self._boxplot_title
        try:
            figure = self._violinplot(data, names, title=title)
        except LinAlgError:
            # Matplotlib doesn't handle single point distributions well
            # in violin plots. Should be fixed in next release:
            # https://github.com/matplotlib/matplotlib/pull/4816
            # Fall back to boxplot
            figure = self._boxplot(data, names, title=title)
        return figure

    @property
    def _winplot_dataset(self):
        # Sort wins by median
        wins = self.result_set.wins
        players = self.result_set.players
        medians = map(median, wins)
        medians = sorted([(m, i) for (i, m) in enumerate(medians)], reverse=True)
        # Reorder and grab names
        wins = [wins[x[-1]] for x in medians]
        ranked_names = [str(players[x[-1]]) for x in medians]
        return wins, ranked_names

    @property
    def _winplot_title(self):
        return ("Distributions of wins:"
                " {} turns repeated {} times ({} strategies)").format(
            self.result_set.turns,
            self.result_set.repetitions,
            len(self.result_set.ranking))

    def winplot(self):
        """Plots the distributions for the number of wins for each strategy."""
        if not self.matplotlib_installed:
            return None

        data, names = self._winplot_dataset
        title = self._winplot_title
        try:
            figure = self._violinplot(data, names, title)
        except LinAlgError:
            # Matplotlib doesn't handle single point distributions well
            # in violin plots. Should be fixed in next release:
            # https://github.com/matplotlib/matplotlib/pull/4816
            # Fall back to boxplot
            figure = self._boxplot(data, names, title)
        # Expand ylim a bit
        maximum = max(max(w) for w in data)
        plt.ylim(-0.5, 0.5 + maximum)
        return figure

    @property
    def _sdv_plot_title(self):
        return ("Distributions of payoff differences per stage game over {} "
                "turns repeated {} times ({} strategies)").format(
            self.result_set.turns,
            self.result_set.repetitions,
            len(self.result_set.ranking))

    @property
    def _sd_ordering(self):
        return self.result_set.ranking

        ## Sort by median then max
        #from operator import itemgetter
        #diffs = self.result_set.score_diffs
        #to_sort = [(median(d), max(d), i) for (i, d) in enumerate(diffs)]
        #to_sort.sort(reverse=True, key=itemgetter(0, 1))
        #ordering = [x[-1] for x in to_sort]
        #return ordering

    @property
    def _sdv_plot_dataset(self):
        ordering = self._sd_ordering
        diffs = self.result_set.score_diffs
        players = self.result_set.players
        # Reorder and grab names
        diffs = [diffs[i] for i in ordering]
        ranked_names = [str(players[i]) for i in ordering]
        return diffs, ranked_names

    def sdvplot(self):
        """Score difference violinplots to visualize the distributions of how
        players attain their payoffs."""
        diffs, ranked_names = self._sdv_plot_dataset
        title = self._sdv_plot_title
        figure = self._violinplot(diffs, ranked_names, title)
        return figure

    ## Payoff heatmaps

    @property
    def _payoff_dataset(self):
        return [[self.result_set.payoff_matrix[r1][r2]
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

    def _payoff_heatmap(self, data, names, title=None):
        """Generic heatmap plot"""
        if not self.matplotlib_installed:
            return None

        nplayers = self.result_set.nplayers
        width = max(nplayers / 4, 12)
        height = width
        figure, ax = plt.subplots()
        figure.set_figwidth(width)
        figure.set_figheight(height)
        cmap = default_cmap()
        mat = ax.matshow(data, cmap=cmap)
        plt.xticks(range(self.result_set.nplayers))
        plt.yticks(range(self.result_set.nplayers))
        ax.set_xticklabels(names, rotation=90)
        ax.set_yticklabels(names)
        plt.tick_params(axis='both', which='both', labelsize=16)
        # Make the colorbar match up with the plot
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", "5%", pad="3%")
        plt.colorbar(mat, cax=cax)
        if title:
            plt.title(title)
        return figure

    def pdplot(self):
        """Payoff difference heatmap to visualize the distributions of how
        players attain their payoffs."""
        matrix, names = self._pdplot_dataset
        return self._payoff_heatmap(matrix, names)

    def payoff(self):
        """Payoff heatmap to visualize the distributions of how
        players attain their payoffs."""
        data = self._payoff_dataset
        names = self.result_set.ranked_names
        return self._payoff_heatmap(data, names)

    ## Ecological Plot

    def stackplot(self, eco):

        if not self.matplotlib_installed:
            return None

        if type(eco) is list:
            warn("""Passing the population sizes as an argument is deprecated and will be removed, please pass the Ecosystem directly""")
            populations = eco
        else:
            populations = eco.population_sizes

        figure, ax = plt.subplots()
        turns = range(len(populations))
        pops = [[populations[iturn][ir] for iturn in turns] for ir in self.result_set.ranking]
        ax.stackplot(turns, *pops)

        ax.yaxis.tick_left()
        ax.yaxis.set_label_position("right")
        ax.yaxis.labelpad = 25.0

        plt.ylim([0.0, 1.0])
        plt.ylabel('Relative population size')
        plt.xlabel('Turn')
        plt.title("Strategy population dynamics based on average payoffs")

        trans = transforms.blended_transform_factory(ax.transAxes, ax.transData)
        ticks = []
        for i, n in enumerate(self.result_set.ranked_names):
            x = -0.01
            y = (i + 0.5) * 1.0 / self.result_set.nplayers
            ax.annotate(n, xy=(x, y), xycoords=trans, clip_on=False, va='center', ha='right', fontsize=5)
            ticks.append(y)
        ax.set_yticks(ticks)
        ax.tick_params(direction='out')
        ax.set_yticklabels([])

        ax.set_xscale('log')

        return figure
