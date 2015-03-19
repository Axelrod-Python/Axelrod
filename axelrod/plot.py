matplotlib_installed = True
try:
    import matplotlib.pyplot as plt
    import matplotlib.transforms as transforms
except ImportError:
    matplotlib_installed = False


class Plot(object):

    def __init__(self, result_set):
        if result_set.finalised:
            self.result_set = result_set
        else:
            raise AttributeError("Result Set is not finalised")
        self.nplayers = self.result_set.nplayers
        self.matplotlib_installed = matplotlib_installed

    def boxplot_dataset(self):
        return [self.result_set.scores[ir] for ir in self.result_set.ranking]

    def payoff_dataset(self):
        return [[self.result_set.payoff_matrix[r1][r2]
                for r2 in self.result_set.ranking]
                for r1 in self.result_set.ranking]

    def boxplot_xticks_locations(self):
        return range(1, len(self.result_set.ranked_names) + 2)

    def boxplot_xticks_labels(self):
        return [str(n) for n in self.result_set.ranked_names]

    def boxplot_title(self):
        return ("Mean score per stage game over {} "
                "rounds repeated {} times ({} strategies)").format(
            self.result_set.turns,
            self.result_set.repetitions,
            len(self.result_set.ranking))

    def boxplot(self):

        if not self.matplotlib_installed:
            return None

        figure = plt.figure()
        plt.boxplot(self.boxplot_dataset())
        plt.xticks(
            self.boxplot_xticks_locations(),
            self.boxplot_xticks_labels(),
            rotation=90)
        plt.tick_params(axis='both', which='both', labelsize=8)
        plt.title(self.boxplot_title())
        return figure

    def payoff(self):

        if not self.matplotlib_installed:
            return None

        figure, ax = plt.subplots()
        mat = ax.matshow(self.payoff_dataset())
        plt.xticks(range(self.result_set.nplayers))
        plt.yticks(range(self.result_set.nplayers))
        ax.set_xticklabels(self.result_set.ranked_names, rotation=90)
        ax.set_yticklabels(self.result_set.ranked_names)
        plt.tick_params(axis='both', which='both', labelsize=8)
        figure.colorbar(mat)
        return figure

    def stackplot(self, populations):

        if not self.matplotlib_installed:
            return None

        figure, ax = plt.subplots()
        turns = range(len(populations))
        pops = [[populations[iturn][ir] for iturn in turns] for ir in self.result_set.ranking]
        ax.stackplot(turns, *pops)

        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.yaxis.labelpad = 25.0

        plt.ylim([0.0, 1.0])
        plt.ylabel('Relative population size')
        plt.xlabel('Turn')
        plt.title("Strategy population dynamics based on average payoffs")

        ax2 = ax.twinx()
        trans = transforms.blended_transform_factory(ax.transAxes, ax.transData)
        ticks = []
        for i, n in enumerate(self.result_set.ranked_names):
            x = -0.02
            y = (i + 0.5) * 1.0 / self.nplayers
            ax.annotate(n, xy=(x, y), xycoords=trans, clip_on=False, va='center', ha='right', fontsize=8)
            ticks.append(y)
        ax.set_yticks(ticks)
        ax.tick_params(direction='out')
        ax.set_yticklabels([])

        return figure
