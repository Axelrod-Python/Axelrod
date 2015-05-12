import math
import csv
from StringIO import StringIO


def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) % 2 == 1:
            return lst[((len(lst)+1)/2)-1]
    if len(lst) % 2 == 0:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0


class ResultSet(object):
    """A class to hold the results of a tournament."""

    unfinalised_error_msg = 'payoffs_list has not been set.'

    def __init__(self, players, turns, repetitions):
        self.players = players
        self.nplayers = len(players)
        self.turns = turns
        self.repetitions = repetitions
        self._init_results()
        self._finalised = False

    # payoffs_list is the only property with a setter method.
    #
    # Setting payoffs_list calls methods to set all the other
    # properties on the instance (result, scores, ranking, ranked_names,
    # payoff_matrix, payoff_stddevs).
    #
    # The getter methods on those other properties will return an error
    # if payoffs_list has not been set.

    @property
    def payoffs_list(self):
        return self._payoffs_list

    @payoffs_list.setter
    def payoffs_list(self, payoffs_list):
        self._payoffs_list = payoffs_list
        self._update_results()
        self._finalised = True
        self._scores = self._generate_scores()
        self._normalised_scores = self._generate_normalised_scores()
        self._ranking = self._generate_ranking(self.scores)
        self._ranked_names = self._generate_ranked_names(self.ranking)
        self._payoff_matrix, self._payoff_stddevs = self._generate_payoff_matrix()

    @payoffs_list.deleter
    def payoffs_list(self):
        del(self._payoffs_list)
        self._init_results()
        self._finalised = False

    @property
    def results(self):
        if self._finalised:
            return self._results
        else:
            raise AttributeError(self.unfinalised_error_msg)

    def _init_results(self):
        plist = list(range(self.nplayers))
        replist = list(range(self.repetitions))
        self._results = [[[0 for r in replist] for j in plist] for i in plist]

    def _update_results(self):
        for index, payoffs in enumerate(self.payoffs_list):
            for i in range(len(self.players)):
                for j in range(len(self.players)):
                    self._results[i][j][index] = payoffs[i][j]

    @property
    def scores(self):
        if self._finalised:
            return self._scores
        else:
            raise AttributeError(self.unfinalised_error_msg)

    def _generate_scores(self):
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
        return scores

    @property
    def normalised_scores(self):
        if self._finalised:
            return self._normalised_scores
        else:
            raise AttributeError(self.unfinalised_error_msg)

    def _generate_normalised_scores(self):
        normalisation = self.turns * (self.nplayers - 1)
        return [
            [1.0 * s / normalisation for s in r] for r in self.scores]

    @property
    def ranking(self):
        if self._finalised:
            return self._ranking
        else:
            raise AttributeError(self.unfinalised_error_msg)

    def _generate_ranking(self, scores):
        """
        Returns a list of players (their index within the
        players list rather than a player instance)
        ordered by median score
        """
        ranking = sorted(
            range(self.nplayers),
            key=lambda i: -median(scores[i]))
        return ranking

    @property
    def ranked_names(self):
        if self._finalised:
            return self._ranked_names
        else:
            raise AttributeError(self.unfinalised_error_msg)

    def _generate_ranked_names(self, ranking):
        """Returns a list of players names sorted by their ranked order."""
        ranked_names = [str(self.players[i]) for i in ranking]
        return ranked_names

    @property
    def payoff_matrix(self):
        if self._finalised:
            return self._payoff_matrix
        else:
            raise AttributeError(self.unfinalised_error_msg)

    @property
    def payoff_stddevs(self):
        if self._finalised:
            return self._payoff_stddevs
        else:
            raise AttributeError(self.unfinalised_error_msg)

    def _generate_payoff_matrix(self):
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
        if self._finalised:
            csv_string = StringIO()
            header = ",".join(self.ranked_names) + "\n"
            csv_string.write(header)
            writer = csv.writer(csv_string, lineterminator="\n")
            for irep in range(self.repetitions):
                data = [self.normalised_scores[rank][irep] for rank in self.ranking]
                writer.writerow(map(str, data))
            return csv_string.getvalue()
        else:
            raise AttributeError(self.unfinalised_error_msg)
