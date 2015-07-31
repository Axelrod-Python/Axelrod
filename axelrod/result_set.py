import math
import csv

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO


def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) % 2 == 1:
            return lst[((len(lst)+1) // 2)-1]
    if len(lst) % 2 == 0:
            return float(sum(lst[(len(lst) // 2)-1:(len(lst) // 2)+1]))/2.0


class ResultSet(object):
    """A class to hold the results of a tournament."""

    def __init__(self, players, turns, repetitions, outcome):
        self.players = players
        self.nplayers = len(players)
        self.turns = turns
        self.repetitions = repetitions
        self.payoffs_list = outcome['payoff']
        self.cooperation_list = outcome['cooperation']
        self.results = self._results_matrix()
        self.scores = self._scores()
        self.normalised_scores = self._normalised_scores()
        self.ranking = self._ranking(self.scores)
        self.ranked_names = self._ranked_names(self.ranking)
        self.payoff_matrix, self.payoff_stddevs = self._payoff_matrix()

    def _null_results_matrix(self):
        plist = list(range(self.nplayers))
        replist = list(range(self.repetitions))
        return [[[0 for r in replist] for j in plist] for i in plist]

    def _results_matrix(self):
        matrix = self._null_results_matrix()
        for index, payoffs in enumerate(self.payoffs_list):
            for i in range(len(self.players)):
                for j in range(len(self.players)):
                    matrix[i][j][index] = payoffs[i][j]
        return matrix

    def _scores(self):
        """Return scores based on the results.

        Originally there were no self-interactions, so the code here was
        rewritten to exclude those from the generated score. To include
        self-interactions, remove the condition on ip and ires and fix the
        normalization factor.
        """
        scores = []
        for ires, res in enumerate(self.results):
            scores.append([])
            for irep in range(self.repetitions):
                scores[-1].append(0)
                for ip in range(self.nplayers):
                    if ip != ires:
                        scores[-1][-1] += res[ip][irep]
        return scores

    def _normalised_scores(self):
        normalisation = self.turns * (self.nplayers - 1)
        return [
            [1.0 * s / normalisation for s in r] for r in self.scores]

    def _ranking(self, scores):
        """
        Returns a list of players (their index within the
        players list rather than a player instance)
        ordered by median score
        """
        ranking = sorted(
            range(self.nplayers),
            key=lambda i: -median(scores[i]))
        return ranking

    def _ranked_names(self, ranking):
        """Returns a list of players names sorted by their ranked order."""
        ranked_names = [str(self.players[i]) for i in ranking]
        return ranked_names

    def _payoff_matrix(self):
        """Returns a per-turn averaged payoff matrix and its stddevs."""
        averages = []
        stddevs = []
        for res in self.results:
            averages.append([])
            stddevs.append([])
            for s in res:
                perturn = [1.0 * rep / self.turns for rep in s]
                avg = sum(perturn) / self.repetitions
                dev = math.sqrt(
                    sum([(avg - pt)**2 for pt in perturn]) / self.repetitions)
                averages[-1].append(avg)
                stddevs[-1].append(dev)
        return averages, stddevs

    def csv(self):
<<<<<<< HEAD
        if self._finalised:
            csv_string = StringIO()
            header = ",".join(self.ranked_names) + "\n"
            csv_string.write(header)
            writer = csv.writer(csv_string, lineterminator="\n")
            for irep in range(self.repetitions):
                data = [self.normalised_scores[rank][irep] for rank in self.ranking]
                writer.writerow(list(map(str, data)))
            return csv_string.getvalue()
        else:
            raise AttributeError(self.unfinalised_error_msg)
=======
        csv_string = StringIO()
        header = ",".join(self.ranked_names) + "\n"
        csv_string.write(header)
        writer = csv.writer(csv_string, lineterminator="\n")
        for irep in range(self.repetitions):
            data = [self.normalised_scores[rank][irep]
                    for rank in self.ranking]
            writer.writerow(map(str, data))
        return csv_string.getvalue()
>>>>>>> refactor resultset to use payoffs and cooperation lists in init
