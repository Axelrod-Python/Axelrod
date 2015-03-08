matplotlib_installed = True
try:
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib_installed = False


class BoxPlot(object):

    def __init__(self, result_set):
        self.result_set = result_set

    def dataset(self):
        return [
            s / (self.result_set.turns *
                 float((len(self.result_set.ranking) - 1)))
            for s in self.result_set.scores[self.result_set.ranking]]

    def xticks_locations(self):
        return range(1, len(self.result_set.ranked_names) + 2)

    def xticks_labels(self):
        return [str(n) for n in self.result_set.ranked_names]

    def title(self):
        return ("Mean score per stage game over {} "
                "rounds repeated {} times ({} strategies)").format(
            self.result_set.turns,
            self.result_set.repetitions,
            len(self.result_set.ranking))

    def figure(self):
        if matplotlib_installed:
            figure = plt.figure()
            plt.boxplot(self.dataset())
            plt.xticks(
                self.xticks_locations(),
                self.xticks_labels(),
                rotation=90)
            plt.title(self.title())
            return figure
        else:
            return None
