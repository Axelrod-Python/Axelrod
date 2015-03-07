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

        self.output_initialised = False

    def generate_scores(self):
        """Returns a numpy array based on the results list"""
        return [[sum([res[ip][irep] for ip in range(self.nplayers)]) for irep in range(self.repetitions)] for res in self.results]

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
        """
        Returns a list of players names sorted by their ranked order.
        """
        ranked_names = [str(self.players[i]) for i in ranking]
        return ranked_names

    def generate_payoff_matrix(self):
        """Returns a per-turn averaged payoff matrix."""
        return [[1.0 * sum(s) / self.turns / self.repetitions for s in r] for r in self.results]

    def init_output(self):
        """
        Sets the scores, ranking and ranked_names properties.
        The output_initialised property ensures that this only done once
        per tournament.
        """
        if not self.output_initialised:
            self.scores = self.generate_scores()
            self.ranking = self.generate_ranking(self.scores)
            self.ranked_names = self.generate_ranked_names(self.ranking)
            self.payoff_matrix = self.generate_payoff_matrix()
            self.output_initialised = True

    def csv(self):
        """Returns a string of csv formatted results"""
        self.init_output()
        csv_string = StringIO()
        header = ",".join(self.ranked_names) + "\n"
        csv_string.write(header)
        writer = csv.writer(csv_string, lineterminator="\n")
        for irep in range(self.repetitions):
            data = [self.scores[rank][irep] for rank in self.ranking]
            writer.writerow(map(str, data))
        return csv_string.getvalue()
