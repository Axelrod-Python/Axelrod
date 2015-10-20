import math
import csv

#from .eigen import *
from axelrod import payoff as ap, cooperation as ac

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO


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
        self.wins = None
        self.cooperation = None
        self.normalised_cooperation = None
        self.vengeful_cooperation = None
        self.cooperating_rating = None
        self.good_partner_matrix = None
        self.good_partner_rating = None
        self.eigenjesus_rating = None
        self.eigenmoses_rating = None

        if 'payoff' in self.results:
            payoff = self.results['payoff']
            self.scores = ap.scores(payoff)
            self.normalised_scores = ap.normalised_scores(self.scores, turns)
            self.ranking = ap.ranking(self.scores)
            self.ranked_names = ap.ranked_names(players, self.ranking)
            self.payoff_matrix, self.payoff_stddevs = (ap.normalised_payoff(
                payoff, turns))
            self.wins = ap.wins(payoff)
            self.payoff_diffs_means = ap.payoff_diffs_means(payoff, turns)
            self.score_diffs = ap.score_diffs(payoff, turns)

        if 'cooperation' in self.results and with_morality:
            self.cooperation = ac.cooperation(self.results['cooperation'])
            self.normalised_cooperation = ac.normalised_cooperation(
                self.cooperation, turns, repetitions)
            self.vengeful_cooperation = ac.vengeful_cooperation(
                self.normalised_cooperation)
            self.cooperating_rating = ac.cooperating_rating(
                self.cooperation, len(players), turns, repetitions)
            self.good_partner_matrix = ac.good_partner_matrix(
                self.results['cooperation'], len(players), repetitions)
            self.good_partner_rating = ac.good_partner_rating(
                self.good_partner_matrix, len(players), repetitions)
            self.eigenjesus_rating = ac.eigenvector(self.normalised_cooperation)
            self.eigenmoses_rating = ac.eigenvector(self.vengeful_cooperation)

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
