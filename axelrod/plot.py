from numpy import arange, median, nan_to_num
import warnings

matplotlib_installed = True
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.transforms as transforms
    from mpl_toolkits.axes_grid1 import make_axes_locatable
except ImportError:
    matplotlib_installed = False
except RuntimeError:
    matplotlib_installed = False
    warnings.warn(
        'Matplotlib failed to import and so no plots will be produced. This ' +
        'could be caused by using a virtual environment on OSX. See ' +
        'http://matplotlib.org/faq/virtualenv_faq.html for details.')


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
        plt.violinplot(data, positions=positions, widths=spacing / 2,
                       showmedians=True, showextrema=False)
        plt.xticks(positions, names, rotation=90)
        plt.xlim(0, spacing * (nplayers + 1))
        plt.tick_params(axis='both', which='both', labelsize=8)
        if title:
            plt.title(title)
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

    def boxplot(self, title=None):
        """For the specific mean score boxplot."""
        data = self._boxplot_dataset
        names = self._boxplot_xticks_labels
        figure = self._violinplot(data, names, title=title)
        return figure

    @property
    def _winplot_dataset(self):
        # Sort wins by median
        wins = self.result_set.wins
        players = self.result_set.players
        medians = map(median, wins)
        medians = sorted(
            [(m, i) for (i, m) in enumerate(medians)], reverse=True)
        # Reorder and grab names
        wins = [wins[x[-1]] for x in medians]
        ranked_names = [str(players[x[-1]]) for x in medians]
        return wins, ranked_names

    def winplot(self, title=None):
        """Plots the distributions for the number of wins for each strategy."""
        if not self.matplotlib_installed:
            return None

        data, names = self._winplot_dataset
        figure = self._violinplot(data, names, title)
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
        diffs = self.result_set.score_diffs
        players = self.result_set.players
        # Reorder and grab names
        diffs = [diffs[i] for i in ordering]
        ranked_names = [str(players[i]) for i in ordering]
        return diffs, ranked_names

    def sdvplot(self, title=None):
        """Score difference violinplots to visualize the distributions of how
        players attain their payoffs."""
        diffs, ranked_names = self._sdv_plot_dataset
        figure = self._violinplot(diffs, ranked_names, title)
        return figure

    @property
    def _lengthplot_dataset(self):
        match_lengths = self.result_set.match_lengths
        return [[length for rep in match_lengths
                 for length in rep[playeri]] for playeri in
                self.result_set.ranking]

    def lengthplot(self, title=None):
        """For the specific match length boxplot."""
        data = self._lengthplot_dataset
        names = self._boxplot_xticks_labels
        figure = self._violinplot(data, names, title=title)
        return figure

    # Payoff heatmaps

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
        if title:
            plt.xlabel(title)
        # Make the colorbar match up with the plot
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", "5%", pad="3%")
        plt.colorbar(mat, cax=cax)
        return figure

    def pdplot(self, title=None):
        """Payoff difference heatmap to visualize the distributions of how
        players attain their payoffs."""
        matrix, names = self._pdplot_dataset
        return self._payoff_heatmap(matrix, names, title)

    def payoff(self, title=None):
        """Payoff heatmap to visualize the distributions of how
        players attain their payoffs."""
        data = self._payoff_dataset
        names = self.result_set.ranked_names
        return self._payoff_heatmap(data, names, title)

    # Ecological Plot

    def stackplot(self, eco, title=None, logscale=True):

        if not self.matplotlib_installed:
            return None

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
        if title is not None:
            plt.title(title)

        trans = transforms.blended_transform_factory(ax.transAxes, ax.transData)
        ticks = []
        for i, n in enumerate(self.result_set.ranked_names):
            x = -0.01
            y = (i + 0.5) * 1.0 / self.result_set.nplayers
            ax.annotate(n, xy=(x, y), xycoords=trans, clip_on=False,
                        va='center', ha='right', fontsize=5)
            ticks.append(y)
        ax.set_yticks(ticks)
        ax.tick_params(direction='out')
        ax.set_yticklabels([])

        if logscale:
            ax.set_xscale('log')

        return figure
