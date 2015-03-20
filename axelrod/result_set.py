import math
import csv

from StringIO import StringIO


def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    if len(lst) %2 == 0:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0


class ResultSet(object):
    """A class to hold the results of a tournament."""

    def __init__(self, players, turns, repetitions):

        self.players = players
        self.nplayers = len(players)

        self.turns = turns
        self.repetitions = repetitions

        plist = list(range(self.nplayers))
        replist = list(range(repetitions))
        self.results = [[[0 for r in replist ] for j in plist] for i in plist]

        self.finalised = False

    def generate_scores(self):
        """Return normalized scores based on the results.

        Originally there were no self-interactions, so the code here was rewritten
        to exclude those from the generated score. To include self-interactions,
        remove the condition on ip and ires and fix the normalization factor.
        """

        scores = []
        for ires, res in enumerate(self.results):
            scores.append([])
            for irep in range(self.repetitions):
                scores[-1].append(0)
                for ip in range(self.nplayers):
                    if ip != ires:
                        scores[-1][-1] += res[ip][irep]

        normalization = self.turns * (self.nplayers - 1)
        scores_normalized = [[1.0 * s / normalization for s in r] for r in scores]

        return scores_normalized

    def generate_ranking(self, scores):
        """
        Returns a list of players (their index within the
        players list rather than a player instance)
        ordered by median score
        """
        ranking = sorted(
            range(self.nplayers),
            key=lambda i: median(scores[i]))
        return ranking

    def generate_ranked_names(self, ranking):
        """Returns a list of players names sorted by their ranked order."""
        ranked_names = [str(self.players[i]) for i in ranking]
        return ranked_names

    def generate_payoff_matrix(self):
        """Returns a per-turn averaged payoff matrix and its stddevs."""
        averages = []
        stddevs = []
        for res in self.results:
            averages.append([])
            stddevs.append([])
            for s in res:
                perturn = [1.0 * rep / self.turns for rep in s]
                avg = sum(perturn) / self.repetitions
                dev = math.sqrt(sum([(avg - pt)**2 for pt in perturn]) / self.repetitions)
                averages[-1].append(avg)
                stddevs[-1].append(dev)
        return averages, stddevs

    def finalise(self, payoffs_list):
        if not self.finalised:
            for index, payoffs in enumerate(payoffs_list):
                for i in range(len(self.players)):
                    for j in range(len(self.players)):
                        self.results[i][j][index] = payoffs[i][j]
            self.scores = self.generate_scores()
            self.ranking = self.generate_ranking(self.scores)
            self.ranked_names = self.generate_ranked_names(self.ranking)
            self.payoff_matrix, self.payoff_stddevs = self.generate_payoff_matrix()
            self.finalised = True
        else:
            raise AttributeError('Result set is already finalised')

    def csv(self):
        if self.finalised:
            csv_string = StringIO()
            header = ",".join(self.ranked_names) + "\n"
            csv_string.write(header)
            writer = csv.writer(csv_string, lineterminator="\n")
            for irep in range(self.repetitions):
                data = [self.scores[rank][irep] for rank in self.ranking]
                writer.writerow(map(str, data))
            return csv_string.getvalue()
        else:
            raise AttributeError("Result Set is not finalised")
