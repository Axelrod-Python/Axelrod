matplotlib_installed = True
try:
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib_installed = False


class Plot(object):

    def __init__(self, result_set):
        self.result_set = result_set
        self.matplotlib_installed = matplotlib_installed

    def boxplot_dataset(self):
        return [self.result_set.scores[ir] for ir in self.result_set.ranking]

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
        if self.matplotlib_installed:
            figure = plt.figure()
            plt.boxplot(self.boxplot_dataset())
            plt.xticks(
                self.boxplot_xticks_locations(),
                self.boxplot_xticks_labels(),
                rotation=90)
            plt.tick_params(axis='both', which='both', labelsize=8)
            plt.title(self.boxplot_title())
            return figure
        else:
            return None
