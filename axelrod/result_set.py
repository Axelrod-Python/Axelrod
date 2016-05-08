from collections import defaultdict
import csv

from numpy import mean, nanmedian, std

from . import eigen
import axelrod.interaction_utils as iu

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO


class ResultSet(object):
    """A class to hold the results of a tournament."""

    def __init__(self, players, interactions, with_morality=True):
        """
        Parameters
        ----------
            players : list
                a list of player objects.
            interactions : list
                a list of dictionaries mapping tuples of player indices to
                interactions (1 for each repetition)
            with_morality : bool
                a flag to determine whether morality metrics should be
                calculated.
        """
        self.players = players
        self.nplayers = len(players)
        self.interactions = interactions
        self.nrepetitions = max([len(rep) for rep in list(interactions.values())])

        # Calculate all attributes:
        self.build_all(with_morality)

    def build_all(self, with_morality):
        """Build all the results. In a seperate method to make inheritance more
        straightforward"""
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

        for index_pair, repetitions in self.interactions.items():
            for repetition, interaction in enumerate(repetitions):
                player, opponent = index_pair
                match_lengths[repetition][player][opponent] = len(interaction)

                if player != opponent:  # Match lengths are symmetric
                    match_lengths[repetition][opponent][player] = len(interaction)

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

        for index_pair, repetitions in self.interactions.items():
            if index_pair[0] != index_pair[1]:  # Ignoring self interactions
                for repetition, interaction in enumerate(repetitions):
                    final_scores = iu.compute_final_score(interaction)
                    for player in range(2):
                        player_index = index_pair[player]
                        player_score = final_scores[player]
                        scores[player_index][repetition] += player_score

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

        for index_pair, repetitions in self.interactions.items():
            if index_pair[0] != index_pair[1]:  # Ignore self interactions
                for player in range(2):
                    player_index = index_pair[player]

                    for rep, interaction in enumerate(repetitions):
                        winner_index = iu.compute_winner_index(interaction)
                        if winner_index is not False and player == winner_index:
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
        for index_pair, repetitions in self.interactions.items():
            for repetition, interaction in enumerate(repetitions):
                if index_pair[0] != index_pair[1]:  # Ignore self interactions
                    scores_per_turn = iu.compute_final_score_per_turn(interaction)
                    for player in range(2):
                        player_index = index_pair[player]
                        score_per_turn = scores_per_turn[player]
                        normalised_scores[player_index][repetition].append(score_per_turn)

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
                      key=lambda i: -nanmedian(self.normalised_scores[i]))

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
        payoffs = [[[] for opponent in plist] for player in plist]

        for player in plist:
            for opponent in plist:
                utilities = []
                for index_pair, repetitions in self.interactions.items():

                    if (player, opponent) == index_pair:
                        for interaction in repetitions:
                            utilities.append(iu.compute_final_score_per_turn(interaction)[0])
                    if (opponent, player) == index_pair:
                        for interaction in repetitions:
                            utilities.append(iu.compute_final_score_per_turn(interaction)[1])

                    payoffs[player][opponent] = utilities
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
        payoff_matrix = [[[] for opponent in plist] for player in plist]

        for player in plist:
            for opponent in plist:
                utilities = self.payoffs[player][opponent]

                if utilities:
                    payoff_matrix[player][opponent] = mean(utilities)
                else:
                    payoff_matrix[player][opponent] = 0

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
        payoff_stddevs = [[[0] for opponent in plist] for player in plist]

        for player in plist:
            for opponent in plist:
                utilities = self.payoffs[player][opponent]

                if utilities:
                    payoff_stddevs[player][opponent] = std(utilities)
                else:
                    payoff_stddevs[player][opponent] = 0

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
        score_diffs = [[[0] * self.nrepetitions for opponent in plist]
                       for player in plist]

        for player in plist:
            for opponent in plist:
                if (player, opponent) in self.interactions:
                    for repetition, interaction in enumerate(self.interactions[(player, opponent)]):
                        scores = iu.compute_final_score_per_turn(interaction)
                        diff = (scores[0] - scores[1])
                        score_diffs[player][opponent][repetition] = diff

                if (opponent, player) in self.interactions:
                    for repetition, interaction in enumerate(self.interactions[(opponent, player)]):
                        scores = iu.compute_final_score_per_turn(interaction)
                        diff = (scores[1] - scores[0])
                        score_diffs[player][opponent][repetition] = diff
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
        payoff_diffs_means = [[0 for opponent in plist] for player in plist]

        for player in plist:
            for opponent in plist:
                diffs = []
                for index_pair, repetitions in self.interactions.items():
                    if (player, opponent) == index_pair:
                        for interaction in repetitions:
                            scores = iu.compute_final_score_per_turn(interaction)
                            diffs.append(scores[0] - scores[1])
                    if (opponent, player) == index_pair:
                        for interaction in repetitions:
                            scores = iu.compute_final_score_per_turn(interaction)
                            diffs.append(scores[1] - scores[0])
                if diffs:
                    payoff_diffs_means[player][opponent] = mean(diffs)
                else:
                    payoff_diffs_means[player][opponent] = 0
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
        cooperations = [[0 for opponent in plist] for player in plist]

        for player in plist:
            for opponent in plist:
                if player != opponent:
                    for index_pair, repetitions in self.interactions.items():
                        coop_count = 0

                        if (player, opponent) == index_pair:
                            for interaction in repetitions:
                                coop_count += iu.compute_cooperations(interaction)[0]
                        if (opponent, player) == index_pair:
                            for interaction in repetitions:
                                coop_count += iu.compute_cooperations(interaction)[1]

                        cooperations[player][opponent] += coop_count
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
        normalised_cooperations = [[0 for opponent in plist] for player in plist]

        for player in plist:
            for opponent in plist:
                coop_counts = []

                if (player, opponent) in self.interactions:
                    repetitions = self.interactions[(player, opponent)]
                    for interaction in repetitions:
                        coop_counts.append(iu.compute_normalised_cooperation(interaction)[0])

                if (opponent, player) in self.interactions:
                    repetitions = self.interactions[(opponent, player)]
                    for interaction in repetitions:
                        coop_counts.append(iu.compute_normalised_cooperation(interaction)[1])

                if ((player, opponent) not in self.interactions) and ((opponent, player) not in self.interactions):
                    coop_counts.append(0)

                # Mean over all reps:
                normalised_cooperations[player][opponent] = mean(coop_counts)
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
        total_length_v_opponent = [zip(*[rep[player_index] for
                                         rep in self.match_lengths])
                                   for player_index in plist]
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
        good_partner_matrix = [[0 for opponent in plist] for player in plist]

        for player in plist:
            for opponent in plist:
                if player != opponent:
                    for index_pair, repetitions in self.interactions.items():

                        if (player, opponent) == index_pair:
                            for interaction in repetitions:
                                coops = iu.compute_cooperations(interaction)
                                if coops[0] >= coops[1]:
                                    good_partner_matrix[player][opponent] += 1

                        if (opponent, player) == index_pair:
                            for interaction in repetitions:
                                coops = iu.compute_cooperations(interaction)
                                if coops[0] <= coops[1]:
                                    good_partner_matrix[player][opponent] += 1

        return good_partner_matrix

    def build_good_partner_rating(self):
        """
        Returns:
        --------

        A list of good partner ratings ordered by player index.
        """
        plist = list(range(self.nplayers))
        good_partner_rating = []

        for player_index in plist:
            total_interactions = 0
            for index_pair, repetitions in self.interactions.items():
                if player_index in index_pair and index_pair[0] != index_pair[1]:
                    total_interactions += len(repetitions)
            # Max is to deal with edge case of matchs with no turns
            rating = sum(self.good_partner_matrix[player_index]) / max(1, float(total_interactions))
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


class ResultSetFromFile(ResultSet):
    """A class to hold the results of a tournament. Reads in a CSV file produced
    by the tournament class.
    """

    def __init__(self, filename, with_morality=True):
        """
        Parameters
        ----------
            filename : string
                name of a file of the correct file.
            with_morality : bool
                a flag to determine whether morality metrics should be
                calculated.
        """
        self.players, self.interactions = self._read_csv(filename)
        self.nplayers = len(self.players)
        self.nrepetitions = len(list(self.interactions.values())[0])

        # Calculate all attributes:
        self.build_all(with_morality)

    def _read_csv(self, filename):
        """
        Reads from a csv file of the format:

        p1index, p2index, p1name, p2name, history1, history2
        ...
        0, 1, Defector, Cooperator, DDD, CCC
        0, 1, Defector, Cooperator, DDD, CCC
        0, 1, Defector, Cooperator, DDD, CCC
        0, 2, Defector, Alternator, DDD, CDC
        0, 2, Defector, Alternator, DDD, CDC
        0, 2, Defector, Alternator, DDD, CDC
        1, 2, Cooperator, Alternator, CCC, CDC
        1, 2, Cooperator, Alternator, CCC, CDC
        1, 2, Cooperator, Alternator, CCC, CDC

        Returns
        -------

            A tuple:
                - First element: list of player names
                - Second element: interactions (a dictionary mapping player pair
                  indices to lists of histories)
        """
        interactions = defaultdict(list)
        players_d = {}
        with open(filename, 'r') as f:
            for row in csv.reader(f):
                index_pair = (int(row[0]), int(row[1]))
                players = (row[2], row[3])
                interaction = list(zip(row[4], row[5]))
                interactions[index_pair].append(interaction)
                # Build a dictionary mapping indices to players
                # This is temporary to make sure the ordering of the players
                # matches the indices
                for index, player in zip(index_pair, players):
                    if index not in players:
                        players_d[index] = player

        # Create an ordered list of players
        players = []
        for i in range(len(players_d)):
            players.append(players_d[i])
        return players, interactions
