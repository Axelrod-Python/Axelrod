class ResultSet(object):
    """
    A class to hold the results of a tournament
    and to return them as plots or csv files.
    """

    def __init__(self, players, repetitions):
        player_list = list(range(len(players)))
        repetition_list = list(range(repetitions))
        self.results = [
            [[0 for irep in repetition_list]
                for j in player_list] for i in player_list]

    def plot(self):
        pass

    def csv(self):
        pass
