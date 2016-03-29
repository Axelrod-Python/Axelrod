import csv
from . import eigen

from numpy import mean, median, std

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO


class ResultSet(object):
    """A class to hold the results of a tournament."""

    def __init__(self, players, matches, with_morality=True):
        """
        Parameters
        ----------
            players : list
                a list of player objects.
            matches : list
                a list of dictionaries mapping tuples of player indices to
                completed matches (1 for each repetition)
            with_morality : bool
                a flag to determine whether morality metrics should be
                calculated.
        """
        self.players = players
        self.nplayers = len(players)
        self.matches = matches
        self.nrepetitions = len(matches)

        # Calculate all attributes:
        self.wins = self.build_wins()
        self.match_lengths = self.build_match_lengths()

        self.scores = self.build_scores()
        self.normalised_scores = self.build_normalised_scores()
        self.ranking = self.build_ranking()
        self.ranked_names = self.build_ranked_names()
        self.payoffs = self.build_payoffs()
        self.payoff_matrix = self.build_payoff_matrix()
        self.payoff_stddevs = self.build_payoff_stddevs()
        self.score_diffs = self.build_score_diffs()
        self.payoff_diffs_means = self.build_payoff_diffs_means()

        if with_morality:
            self.cooperation = self.build_cooperation()
            self.normalised_cooperation = self.build_normalised_cooperation()
            self.vengeful_cooperation = self.build_vengeful_cooperation()
            self.cooperating_rating = self.build_cooperating_rating()
            self.good_partner_matrix = self.build_good_partner_matrix()
            self.good_partner_rating = self.build_good_partner_rating()
            self.eigenmoses_rating = self.build_eigenmoses_rating()
            self.eigenjesus_rating = self.build_eigenjesus_rating()

    @property
    def _null_results_matrix(self):
        """
        Returns:
        --------
            A null matrix (i.e. fully populated with zero values) using
            lists of the form required for the results dictionary.

            i.e. one row per player, containing one element per opponent (in
            order of player index) which lists values for each repetition.
        """
        plist = list(range(self.nplayers))
        replist = list(range(self.nrepetitions))
        return [[[0 for j in plist] for i in plist] for r in replist]

    def build_match_lengths(self):
        """
        Returns:
        --------
            The match lengths. List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of repetitions and MLi is a list of the form:

            [Pli1, PLi2, Pli3, ..., Plim]

            Where m is the number of players and Plij is of the form:

            [aij1, aij2, aij3, ..., aijk]

            Where k is the number of players and aijk is the length of the match
            between player j and k in repetition i.
        """
        match_lengths = self._null_results_matrix

        for rep in range(self.nrepetitions):

            for player_pair_index, match in self.matches[rep].items():
                i, j = player_pair_index
                match_lengths[rep][i][j] = len(match)

                if i != j:  # Match lengths are symmetric
                    match_lengths[rep][j][i] = len(match)

        return match_lengths

    def build_scores(self):
        """
        Returns:
        --------
            The total scores per player for each repetition lengths.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where m is the number of repetitions and pij is the total score
            obtained by each player in repetition j.

            In Axelrod's original tournament, there were no self-interactions
            (e.g. player 1 versus player 1) and so these are also ignored.
        """
        scores = [[0 for rep in range(self.nrepetitions)] for _ in
                  range(self.nplayers)]

        for rep, matches_dict in enumerate(self.matches):
            for index_pair, match in matches_dict.items():
                if index_pair[0] != index_pair[1]: # Ignoring self interactions
                    for player in range(2):
                        player_index = index_pair[player]
                        player_score = match.final_score()[player]
                        scores[player_index][rep] += player_score

        return scores

    def build_ranked_names(self):
        """
        Returns:
        --------
            Returns the ranked names. A list of names as calculated by
            self.ranking.
        """
        return [str(self.players[i]) for i in self.ranking]

    def build_wins(self):
        """
        Returns:
        --------

            The total wins per player for each repetition lengths.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where m is the number of repetitions and pij is the total wins
            obtained by each player in repetition j.

            In Axelrod's original tournament, there were no self-interactions
            (e.g. player 1 versus player 1) and so these are also ignored.
        """
        wins = [[0 for rep in range(self.nrepetitions)] for _ in
                range(self.nplayers)]

        for rep, matches_dict in enumerate(self.matches):
            for index_pair, match in matches_dict.items():
                if index_pair[0] != index_pair[1]:  # Ignore self interactions
                    for player in range(2):
                        player_index = index_pair[player]

                        if match.players[player] == match.winner():
                            wins[player_index][rep] += 1

        return wins

    def build_normalised_scores(self):
        """
        Returns:
        --------

            The total mean scores per turn per layer for each repetition
            lengths.  List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where m is the number of repetitions and pij is the mean scores per
            turn obtained by each player in repetition j.

            In Axelrod's original tournament, there were no self-interactions
            (e.g. player 1 versus player 1) and so these are also ignored.
        """
        normalised_scores = [
            [[] for rep in range(self.nrepetitions)] for _ in
            range(self.nplayers)]

        # Getting list of all per turn scores for each player for each rep
        for rep, matches_dict in enumerate(self.matches):
            for index_pair, match in matches_dict.items():
                if index_pair[0] != index_pair[1]:  # Ignore self interactions
                    for player in range(2):
                        player_index = index_pair[player]
                        score_per_turn = match.final_score_per_turn()[player]
                        normalised_scores[player_index][rep].append(score_per_turn)

        # Obtaining mean scores and overwriting corresponding entry in
        # normalised scores
        for i, rep in enumerate(normalised_scores):
            for j, player_scores in enumerate(rep):
                normalised_scores[i][j] = mean(player_scores)

        return normalised_scores

    def build_ranking(self):
        """
        Returns:
        --------

            The ranking. List of the form:

            [R1, R2, R3..., Rn]

            Where n is the number of players and Rj is the rank of the jth player
            (based on median normalised score).
        """
        return sorted(range(self.nplayers),
                      key=lambda i: -median(self.normalised_scores[i]))

    def build_payoffs(self):
        """
        Returns:
        --------

            The list of per turn payoffs.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where m is the number of players and pij is a list of the form:

            [uij1, uij2, ..., uijk]

            Where k is the number of repetitions and uijk is the list of utilities
            obtained by player i against player j in each repetition.
        """
        plist = list(range(self.nplayers))
        payoffs = [[[] for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                utilities = []
                for rep in self.matches:

                    if (i, j) in rep:
                        match = rep[(i, j)]
                        utilities.append(match.final_score_per_turn()[0])
                    if (j, i) in rep:
                        match = rep[(j, i)]
                        utilities.append(match.final_score_per_turn()[1])

                    payoffs[i][j] = utilities
        return payoffs

    def build_payoff_matrix(self):
        """
        Returns:
        --------
            The mean of per turn payoffs.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where m is the number of players and pij is a list of the form:

            [uij1, uij2, ..., uijk]

            Where k is the number of repetitions and u is the mean utility (over
            all repetitions) obtained by player i against player j.
        """
        plist = list(range(self.nplayers))
        payoff_matrix = [[[0] for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                utilities = self.payoffs[i][j]

                if utilities:
                    payoff_matrix[i][j] = mean(utilities)
                else:
                    payoff_matrix[i][j] = 0

        return payoff_matrix

    def build_payoff_stddevs(self):
        """
        Returns:
        --------

            The mean of per turn payoffs.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where m is the number of players and pij is a list of the form:

            [uij1, uij2, ..., uijk]

            Where k is the number of repetitions and u is the standard
            deviation of the utility (over all repetitions) obtained by player
            i against player j.
        """
        plist = list(range(self.nplayers))
        payoff_stddevs = [[[0] for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                utilities = self.payoffs[i][j]

                if utilities:
                    payoff_stddevs[i][j] = std(utilities)
                else:
                    payoff_stddevs[i][j] = 0

        return payoff_stddevs

    def build_score_diffs(self):
        """
        Returns:
        --------

            Returns the score differences between players.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where m is the number of players and pij is a list of the form:

            [uij1, uij2, ..., uijk]

            Where k is the number of repetitions and uijm is the difference of the
            scores per turn between player i and j in repetition m.
        """
        plist = list(range(self.nplayers))
        score_diffs = [[[0] * self.nrepetitions for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                for r, rep in enumerate(self.matches):
                    if (i, j) in rep:
                        scores = rep[(i, j)].final_score_per_turn()
                        diff = (scores[0] - scores[1])
                        score_diffs[i][j][r] = diff
                    if (j, i) in rep:
                        scores = rep[(j, i)].final_score_per_turn()
                        diff = (scores[1] - scores[0])
                        score_diffs[i][j][r] = diff
        return score_diffs

    def build_payoff_diffs_means(self):
        """
        Returns:
        --------

            The score differences between players.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where pij is the mean difference of the
            scores per turn between player i and j in repetition m.
        """
        plist = list(range(self.nplayers))
        payoff_diffs_means = [[0 for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                diffs = []
                for rep in self.matches:
                    if (i, j) in rep:
                        scores = rep[(i, j)].final_score_per_turn()
                        diffs.append(scores[0] - scores[1])
                    if (j, i) in rep:
                        scores = rep[(j, i)].final_score_per_turn()
                        diffs.append(scores[1] - scores[0])
                if diffs:
                    payoff_diffs_means[i][j] = mean(diffs)
                else:
                    payoff_diffs_means[i][j] = 0
        return payoff_diffs_means

    def build_cooperation(self):
        """
        Returns:
        --------

            The list of cooperation counts.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where pij is the total number of cooperations over all repetitions
            played by player i against player j.
        """
        plist = list(range(self.nplayers))
        cooperations = [[0 for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                if i != j:
                    for rep in self.matches:
                        coop_count = 0

                        if (i, j) in rep:
                            match = rep[(i, j)]
                            coop_count = match.cooperation()[0]
                        if (j, i) in rep:
                            match = rep[(j, i)]
                            coop_count = match.cooperation()[1]

                        cooperations[i][j] += coop_count
        return cooperations

    def build_normalised_cooperation(self):
        """
        Returns:
        --------

            The list of per turn cooperation counts.
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pin]

            Where pij is the mean number of
            cooperations per turn played by player i against player j in each
            repetition.
        """
        plist = list(range(self.nplayers))
        normalised_cooperations = [[0 for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                coop_counts = []
                for rep in self.matches:

                    if (i, j) in rep:
                        match = rep[(i, j)]
                        coop_counts.append(match.normalised_cooperation()[0])

                    if (j, i) in rep:
                        match = rep[(j, i)]
                        coop_counts.append(match.normalised_cooperation()[1])

                    if ((i, j) not in rep) and ((j, i) not in rep):
                        coop_counts.append(0)

                    # Mean over all reps:
                    normalised_cooperations[i][j] = mean(coop_counts)
        return normalised_cooperations

    def build_vengeful_cooperation(self):
        """
        Returns:
        --------

            The vengeful cooperation matrix derived from the
            normalised cooperation matrix:

                Dij = 2(Cij - 0.5)
        """
        return [[2 * (element - 0.5) for element in row]
                for row in self.normalised_cooperation]

    def build_cooperating_rating(self):
        """
        Returns:
        --------

            The list of cooperation counts
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where pij is the total number of cooperations divided by the total
            number of turns over all repetitions played by player i against
            player j.
        """

        plist = list(range(self.nplayers))
        total_length_v_opponent = [zip(*[rep[playeri] for
                                         rep in self.match_lengths])
                                   for playeri in plist]
        lengths = [[sum(e) for j, e in enumerate(row) if i != j] for i, row in
                   enumerate(total_length_v_opponent)]

        # Max is to deal with edge cases of matches that have no turns
        return [sum(cs) / max(1, float(sum(ls))) for cs, ls
                in zip(self.cooperation, lengths)]

    def build_good_partner_matrix(self):
        """
        Returns:
        --------

            An n by n matrix of good partner ratings for n players i.e. an n by
            n matrix where n is the number of players. Each row (i) and column
            (j) represents an individual player and the value Pij is the sum of
            the number of repetitions where player i cooperated as often or
            more than opponent j.
        """

        plist = list(range(self.nplayers))
        good_partner_matrix = [[0 for j in plist] for i in plist]

        for i in plist:
            for j in plist:
                if i != j:
                    for rep in self.matches:

                        if (i, j) in rep:
                            match = rep[(i, j)]
                            coops = match.cooperation()
                            if coops[0] >= coops[1]:
                                good_partner_matrix[i][j] += 1

                        if (j, i) in rep:
                            match = rep[(j, i)]
                            coops = match.cooperation()
                            if coops[0] <= coops[1]:
                                good_partner_matrix[i][j] += 1

        return good_partner_matrix

    def build_good_partner_rating(self):
        """
        Returns:
        --------

        A list of good partner ratings ordered by player index.
        """
        plist = list(range(self.nplayers))
        good_partner_rating = []

        for playeri in plist:
            total_interactions = 0
            for rep in self.matches:
                total_interactions += len(
                    [pair for pair in rep.keys()
                     if playeri in pair and pair[0] != pair[1]])
            # Max is to deal with edge case of matchs with no turns
            rating = sum(self.good_partner_matrix[playeri]) / max(1, float(total_interactions))
            good_partner_rating.append(rating)

        return good_partner_rating

    def build_eigenjesus_rating(self):
        """
        Returns:
        --------

        The eigenjesus rating as defined in:
        http://www.scottaaronson.com/morality.pdf
        """
        eigenvector, eigenvalue = eigen.principal_eigenvector(
                self.normalised_cooperation)
        return eigenvector.tolist()

    def build_eigenmoses_rating(self):
        """
        Returns:
        --------

        The eigenmoses rating as defined in:
        http://www.scottaaronson.com/morality.pdf
        """
        eigenvector, eigenvalue = eigen.principal_eigenvector(
                self.vengeful_cooperation)
        return eigenvector.tolist()

    def csv(self):
        """
        Returns:
        --------

        The string of the total scores per player (columns) per repetition
        (rows).
        """
        csv_string = StringIO()
        header = ",".join(self.ranked_names) + "\n"
        csv_string.write(header)
        writer = csv.writer(csv_string, lineterminator="\n")
        for irep in range(self.nrepetitions):
            data = [self.normalised_scores[rank][irep]
                    for rank in self.ranking]
            writer.writerow(list(map(str, data)))
        return csv_string.getvalue()
