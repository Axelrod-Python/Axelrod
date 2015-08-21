import math
import csv
from .eigen import *

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

    def __init__(self, players, turns, repetitions, outcome,
                 with_morality=True):
        """
        Args:
            players (list): a list of player objects.
            turns (int): the number of turns per interaction.
            repetitions (int): the number of time the round robin was repeated.
            outcome (dict): returned from the RoundRobin class and containing
                various sets of results for processing by this class.
            with_morality (bool): a flag to determine whether morality metrics
                should be calculated.
        """
        self.players = players
        self.nplayers = len(players)
        self.turns = turns
        self.repetitions = repetitions
        self.outcome = outcome
        self.results = self._results(outcome)
        self.scores = None
        self.normalised_scores = None
        self.ranking = None
        self.ranked_names = None
        self.payoff_matrix = None
        self.cooperation = None
        self.normalised_cooperation = None
        self.vengeful_cooperation = None
        self.cooperating_rating = None
        self.good_partner_matrix = None
        self.good_partner_rating = None
        self.eigenjesus_rating = None
        self.eigenmoses_rating = None
        if 'payoff' in self.results:
            self.scores = self._scores(self.results['payoff'])
            self.normalised_scores = self._normalised_scores(self.scores)
            self.ranking = self._ranking(self.scores)
            self.ranked_names = self._ranked_names(self.ranking)
            self.payoff_matrix, self.payoff_stddevs = (
                self._payoff_matrix(self.results['payoff']))
        if 'cooperation' in self.results and with_morality:
            self.cooperation = self._cooperation(self.results['cooperation'])
            self.normalised_cooperation = (
                self._normalised_cooperation(self.cooperation))
            self.vengeful_cooperation = (
                self._vengeful_cooperation(self.normalised_cooperation))
            self.cooperating_rating = self._cooperating_rating(self.cooperation)
            self.good_partner_matrix = (
                self._good_partner_matrix(self.results['cooperation']))
            self.good_partner_rating = (
                self._good_partner_rating(self.good_partner_matrix))
            self.eigenjesus_rating = (
                self._eigenvector(self.normalised_cooperation))
            self.eigenmoses_rating = (
                self._eigenvector(self.vengeful_cooperation))

    @property
    def _null_results_matrix(self):
        """
        Returns:
            A null matrix (i.e. fully populated with zero values) using
            lists of the form required for the results dictionary.

            i.e. one row per player, containing one element per opponent (in order
            of player index) which lists values for each repetition.
        """
        plist = list(range(self.nplayers))
        replist = list(range(self.repetitions))
        return [[[0 for r in replist] for j in plist] for i in plist]

    @property
    def _null_matrix(self):
        """
        Returns:
            A null n by n matrix where n is the number of players.
        """
        plist = list(range(self.nplayers))
        return [[0 for j in plist] for i in plist]

    def _results(self, outcome):
        """
        Args:
            outcome(dict): the outcome dictionary, in which the values are
                lists of the form:

                    [
                        [[a, b, c], [d, e, f], [g, h, i]],
                        [[j, k, l], [m, n, o], [p, q, r]],
                    ]

                i.e. one row per repetition, containing one element per player,
                which lists values for each opponent in order of player index.

        Returns:
            A results dictionary, in which the values are lists of
            the form:

                [
                    [[a, j], [b, k], [c, l]],
                    [[d, m], [e, n], [f, o]],
                    [[g, p], [h, q], [i, r]],
                ]

            i.e. one row per player, containing one element per opponent (in order
            of player index) which lists values for each repetition.
        """
        results = {}
        for result_type, result_list in outcome.items():
            matrix = self._null_results_matrix
            for index, result_matrix in enumerate(result_list):
                for i in range(len(self.players)):
                    for j in range(len(self.players)):
                        matrix[i][j][index] = result_matrix[i][j]
                results[result_type] = matrix
        return results

    def _scores(self, payoff):
        """
        Args:
            payoff (list): a matrix of the form:

                [
                    [[a, j], [b, k], [c, l]],
                    [[d, m], [e, n], [f, o]],
                    [[g, p], [h, q], [i, r]],
                ]

            i.e. one row per player, containing one element per opponent (in
            order of player index) which lists payoffs for each repetition.

        Returns:
            A scores matrix of the form:

                [
                    [a + b + c, j + k + l],
                    [d + e + f, m + n+ o],
                    [h + h + i, p + q + r],
                ]

            i.e. one row per player which lists the total score for each
            repetition.

        In Axelrod's original tournament, there were no self-interactions
        (e.g. player 1 versus player 1) and so these are also excluded from the
        scores here by the condition on ip and ires.
        """
        scores = []
        for ires, res in enumerate(payoff):
            scores.append([])
            for irep in range(self.repetitions):
                scores[-1].append(0)
                for ip in range(self.nplayers):
                    if ip != ires:
                        scores[-1][-1] += res[ip][irep]
        return scores

    def _normalised_scores(self, scores):
        """
        Args:
            scores (list): the scores matrix (S)

        Returns:
            A normalised scores matrix (N) such that:

                N = S / t

            where t is the total number of turns played per repetition for a given
            player excluding self-interactions.
        """
        normalisation = self.turns * (self.nplayers - 1)
        return [
            [1.0 * s / normalisation for s in r] for r in scores]

    def _ranking(self, scores):
        """
        Args:
            scores (list): the scores matrix (S)

        Returns:
            A list of players (their index within the players list rather than
            a player instance) ordered by median score
        """
        ranking = sorted(
            range(self.nplayers),
            key=lambda i: -median(scores[i]))
        return ranking

    def _ranked_names(self, ranking):
        """
        Args:
            ranking (list): A list of player index numbers

        Returns:
             A list of players names sorted by their ranked order.
        """
        ranked_names = [str(self.players[i]) for i in ranking]
        return ranked_names

    def _payoff_matrix(self, payoff):
        """
        Args:
            payoff (list): a matrix of the form:

                [
                    [[a, j], [b, k], [c, l]],
                    [[d, m], [e, n], [f, o]],
                    [[g, p], [h, q], [i, r]],
                ]

            i.e. one row per player, containing one element per opponent (in
            order of player index) which lists payoffs for each repetition.

        Returns:
            A per-turn averaged payoff matrix and its stddevs.
        """
        averages = []
        stddevs = []
        for res in payoff:
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

    def _cooperation(self, results):
        """
        Args:
            results (list): a matrix of the form:

                [
                    [[a, j], [b, k], [c, l]],
                    [[d, m], [e, n], [f, o]],
                    [[g, p], [h, q], [i, r]],
                ]

            i.e. one row per player, containing one element per opponent (in
            order of player index) which lists cooperation values for each
            repetition.

        Returns:
            The cooperation matrix (C) of the form:

                [
                    [[a + j], [b + k], [c + l]],
                    [[d + m], [e + n], [f + o]],
                    [[g + p], [h + q], [i + r]],
                ]

            i.e. an n by n matrix where n is the number of players. Each row (i)
            andcolumn (j) represents an individual player and the the value Cij
            is the number of times player i cooperated against opponent j.
        """
        return[[sum(element) for element in row] for row in results]

    def _normalised_cooperation(self, cooperation):
        """
        Args:
            cooperation (list): the cooperation matrix (C)

        Returns:
            A matrix (N) such that:

                N = C / t

            where t is the total number of turns played in the tournament.
        """
        turns = self.turns * self.repetitions
        return[
            [1.0 * element / turns for element in row]
            for row in cooperation]

    def _vengeful_cooperation(self, cooperation):
        """
        Args:
            cooperation(list): A cooperation matrix (C)

        Returns:
            A matrix (D) such that:

                Dij = 2(Cij -0.5)
        """
        return [[2 * (element - 0.5) for element in row] for row in cooperation]

    def _cooperating_rating(self, cooperation):
        """
        Args:
            cooperation (list): the cooperation matrix

        Returns:
            a list of cooperation rates ordered by player index"""
        total_turns = self.turns * self.repetitions * self.nplayers
        return [1.0 * sum(row) / total_turns for row in cooperation]

    def _good_partner_matrix(self, results):
        """
        Args:
            results (list): cooperation results matrix of the form:

                [
                    [[a, j], [b, k], [c, l]],
                    [[d, m], [e, n], [f, o]],
                    [[g, p], [h, q], [i, r]],
                ]

            i.e. one row per player, containing one element per opponent (in
            order of player index) which lists cooperation values for each
            repetition.

        Returns:
            The good partner matrix (P) of the form:

                [
                    [0, 0 + (1 if b >= d) + (1 if k >= m), 0 + (1 if c >= g) + (1 if l >= p) ],
                    [0 + (1 if e >= g) + (1 if n >= p), 0, 0 + (1 if f >= h) + (1 if o >= q)],
                    [0 + (1 if g >= c) + (1 if p >= l), 0 + (1 if h >= f) + (1 if q >= o), 0]
                ]

            i.e. an n by n matrix where n is the number of players. Each row (i)
            and column (j) represents an individual player and the the value Pij
            is the sum of the number of repetitions where player i cooperated as
            often or more than opponent j.
        """
        matrix = self._null_matrix
        for r in range(self.repetitions):
            for i in range(self.nplayers):
                for j in range(self.nplayers):
                    if i != j and results[i][j][r] >= results[j][i][r]:
                        matrix[i][j] += 1
        return matrix

    @property
    def _interactions(self):
        """
        Returns:
            the number of interactions between players excluding
            self-interactions.
        """
        return self.repetitions * (self.nplayers - 1)

    def _good_partner_rating(self, good_partner):
        """
        Args:
            good_partner (list): the good partner matrix

        Returns:
            a list of good partner ratings ordered by player index.
        """
        return [1.0 * sum(row) / self._interactions for row in good_partner]

    def _eigenvector(self, cooperation):
        """
        Args:
            cooperation (list): a cooperation matrix

        Returns:
            the principal eigenvector of the cooperation matrix as a list.
        """
        eigenvector, eigenvalue = principal_eigenvector(cooperation, 1000, 1e-3)
        return eigenvector.tolist()

    def csv(self):
        csv_string = StringIO()
        header = ",".join(self.ranked_names) + "\n"
        csv_string.write(header)
        writer = csv.writer(csv_string, lineterminator="\n")
        for irep in range(self.repetitions):
            data = [self.normalised_scores[rank][irep]
                    for rank in self.ranking]
            writer.writerow(list(map(str, data)))
        return csv_string.getvalue()
