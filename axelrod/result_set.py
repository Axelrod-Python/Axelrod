import numpy
from StringIO import StringIO
import matplotlib.pyplot as plt


class ResultSet(object):
    """
    A class to hold the results of a tournament
    and to return them as plots or csv files.
    """

    def __init__(self, players, turns, repetitions):
        self.players = players
        self.nplayers = len(players)
        player_list = list(range(len(players)))
        self.turns = turns
        self.repetitions = repetitions
        repetition_list = list(range(repetitions))
        self.results = [
            [[0 for irep in repetition_list]
                for j in player_list] for i in player_list]
        self.output_initialised = False

    def generate_scores(self):
        numpy_array_results = numpy.array(self.results)
        return numpy_array_results.sum(axis=1)

    def generate_ranking(self, scores):
        ranking = sorted(
            range(self.nplayers),
            key=lambda i: numpy.median(scores[i]))
        return ranking

    def generate_ranked_names(self, ranking):
        ranked_names = [str(self.players[i]) for i in ranking]
        return ranked_names

    def init_output(self):
        if not self.output_initialised:
            self.scores = self.generate_scores()
            self.ranking = self.generate_ranking(self.scores)
            self.ranked_names = self.generate_ranked_names(self.ranking)
            self.output_initialised = True

    def plot(self):
        self.init_output()
        fig = plt.figure()
        plt.boxplot([s / (self.turns * (len(self.ranking) - 1)) for s in self.scores[self.ranking]])
        plt.xticks(range(1, len(self.ranked_names) + 2), [str(n) for n in self.ranked_names], rotation=90)
        plt.title('Mean score per stage game over {} rounds repeated {} times ({} strategies)'.format(self.turns, self.repetitions, len(self.ranking)))
        return fig

    def csv(self):
        self.init_output()
        csv_string = StringIO()
        header = ", ".join(self.ranked_names) + "\n"
        csv_string.write(header)
        numpy.savetxt(
            csv_string,
            self.scores[self.ranking].transpose(),
            delimiter=", ",
            fmt='%i')
        return csv_string.getvalue()
