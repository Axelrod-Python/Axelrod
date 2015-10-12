#from operator import itemgetter

from numpy import arange, mean, median

matplotlib_installed = True
try:
    import matplotlib.pyplot as plt
    import matplotlib.transforms as transforms
    from mpl_toolkits.axes_grid1 import make_axes_locatable
except ImportError:
    matplotlib_installed = False


class Plot(object):

    def __init__(self, result_set):
        self.result_set = result_set
        self.matplotlib_installed = matplotlib_installed

    @property
    def _boxplot_dataset(self):
        return [self.result_set.normalised_scores[ir] for ir in self.result_set.ranking]

    @property
    def _payoff_dataset(self):
        return [[self.result_set.payoff_matrix[r1][r2]
                for r2 in self.result_set.ranking]
                for r1 in self.result_set.ranking]

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

        if not self.matplotlib_installed:
            return None

        figure = plt.figure()
        plt.boxplot(self._boxplot_dataset)
        plt.xticks(
            self._boxplot_xticks_locations,
            self._boxplot_xticks_labels,
            rotation=90)
        plt.tick_params(axis='both', which='both', labelsize=7)
        plt.title(self._boxplot_title)
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

    def vplot(self, data, names):
        if not self.matplotlib_installed:
            return None
        nplayers = self.result_set.nplayers
        width = max(nplayers / 2, 12)
        height = width / 4
        figure = plt.figure(figsize=(width, height))
        spacing = 4
        positions = spacing * arange(1, nplayers + 1, 1)
        plt.violinplot(data, positions=positions, widths=spacing / 2,
                       showmedians=True)
        plt.xticks(
            positions,
            names,
            rotation=90)
        plt.xlim(0, spacing * (nplayers + 1))
        plt.tick_params(axis='both', which='both', labelsize=7)
        plt.title(self._sdv_plot_title)
        return figure

    #def bplot(self, data, names):
        #if not self.matplotlib_installed:
            #return None

        #figure = plt.figure()
        #plt.boxplot(data)
        #plt.xticks(
            #self._boxplot_xticks_locations,
            #names,
            #rotation=90)
        #plt.tick_params(axis='both', which='both', labelsize=7)
        #plt.title(self._boxplot_title)
        #return figure





    def sdvplot(self):
        """Score difference violinplots to visualize the distributions of how
        players attain their payoffs."""

        if not self.matplotlib_installed:
            return None

        diffs, ranked_names = self._sdv_plot_dataset
        figure = self.vplot(diffs, ranked_names)
        return figure

        if not self.matplotlib_installed:
            return None
        diffs, ranked_names = self._sdv_plot_dataset
        nplayers = self.result_set.nplayers
        width = max(nplayers / 2, 12)
        height = width / 4
        figure = plt.figure(figsize=(width, height))
        spacing = 4
        positions = spacing * arange(1, nplayers + 1, 1)
        plt.violinplot(diffs, positions=positions, widths=spacing / 2,
                       showmedians=True)
        plt.xticks(
            #self._boxplot_xticks_locations,
            positions,
            ranked_names,
            rotation=90)
        plt.xlim(0, spacing * (nplayers + 1))
        plt.tick_params(axis='both', which='both', labelsize=7)
        plt.title(self._sdv_plot_title)
        return figure

    @property
    def _pdplot_dataset(self):
        # Order like the sdv_plot
        ordering = self._sd_ordering
        pdm = self.result_set.payoff_diffs_matrix
        # Reorder and grab names
        matrix = [[pdm[r1][r2] for r2 in ordering]
                  for r1 in ordering]
        players = self.result_set.players
        ranked_names = [str(players[i]) for i in ordering]
        return matrix, ranked_names

    def pdplot(self):
        """Payoff difference heatmap to visualize the distributions of how
        players attain their payoffs."""
        if not self.matplotlib_installed:
            return None

        matrix, ranked_names = self._pdplot_dataset
        figure, ax = plt.subplots()
        mat = ax.matshow(matrix, cmap='YlGnBu')
        plt.xticks(range(self.result_set.nplayers))
        plt.yticks(range(self.result_set.nplayers))
        ax.set_xticklabels(ranked_names, rotation=90)
        ax.set_yticklabels(ranked_names)
        plt.tick_params(axis='both', which='both', labelsize=6)
        # Make the colorbar match up with the plot
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", "5%", pad="3%")
        plt.colorbar(mat, cax=cax)
        return figure

    @property
    def _winplot_dataset(self):
        # Sort wins by median
        wins = self.result_set.wins
        players = self.result_set.players
        medians = map(median, wins)
        medians = sorted([(m, i) for (i, m) in enumerate(medians)], reverse=True)
        # Reorder and grab names
        wins = [wins[x[1]] for x in medians]
        ranked_names = [str(players[x[1]]) for x in medians]
        return wins, ranked_names

    @property
    def _winplot_title(self):
        return ("Distributions of wins:"
                " {} turns repeated {} times ({} strategies)").format(
            self.result_set.turns,
            self.result_set.repetitions,
            len(self.result_set.ranking))

    def winplot(self):
        if not self.matplotlib_installed:
            return None

        wins, ranked_names = self._winplot_dataset
        maximum = max(max(w) for w in wins)

        figure = plt.figure()
        plt.boxplot(wins)
        plt.xticks(
            self._boxplot_xticks_locations,
            ranked_names,
            rotation=90)
        plt.tick_params(axis='both', which='both', labelsize=7)
        plt.title(self._winplot_title)
        plt.ylim(-0.5, 0.5 + maximum)
        return figure

    def payoff(self):

        if not self.matplotlib_installed:
            return None

        figure, ax = plt.subplots()
        mat = ax.matshow(self._payoff_dataset, cmap='YlGnBu')
        plt.xticks(range(self.result_set.nplayers))
        plt.yticks(range(self.result_set.nplayers))
        ax.set_xticklabels(self.result_set.ranked_names, rotation=90)
        ax.set_yticklabels(self.result_set.ranked_names)
        plt.tick_params(axis='both', which='both', labelsize=6)
        # Make the colorbar match up with the plot
        divider = make_axes_locatable(plt.gca())
        cax = divider.append_axes("right", "5%", pad="3%")
        plt.colorbar(mat, cax=cax)
        return figure

    def stackplot(self, populations):

        if not self.matplotlib_installed:
            return None

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
