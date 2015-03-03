import numpy
from StringIO import StringIO


class ResultSet(object):
    """
    A class to hold the results of a tournament
    and to return them as plots or csv files.
    """

    def __init__(self, players, repetitions):
        self.players = players
        player_list = list(range(len(players)))
        repetition_list = list(range(repetitions))
        self.results = [
            [[0 for irep in repetition_list]
                for j in player_list] for i in player_list]

    def scores(self):
        numpy_array_results = numpy.array(self.results)
        return numpy_array_results.sum(axis=1)

    def plot(self):
        pass

    def csv(self):
        nplayers = len(self.players)
        scores = self.scores()
        ranking = sorted(
            range(nplayers),
            key=lambda i: numpy.median(scores[i]))
        ranked_names = [str(self.players[i]) for i in ranking]
        csv_string = StringIO()
        header = ", ".join(ranked_names) + "\n"
        csv_string.write(header)
        numpy.savetxt(
            csv_string,
            scores[ranking].transpose(),
            delimiter=", ",
            fmt='%i')
        return csv_string.getvalue()
