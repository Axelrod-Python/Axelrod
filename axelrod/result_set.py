from collections import namedtuple, Counter
from multiprocessing import cpu_count
import csv
import itertools

from numpy import mean, nanmedian, std, array, nan_to_num
import tqdm

import dask as da
import dask.dataframe as dd

from axelrod.action import Action, str_to_actions
import axelrod.interaction_utils as iu
from . import eigen
from .game import Game


C, D = Action.C, Action.D


def update_progress_bar(method):
    """A decorator to update a progress bar if it exists"""
    def wrapper(*args):
        """Run the method and update the progress bar if it exists"""
        output = method(*args)

        try:
            args[0].progress_bar.update(1)
        except AttributeError:
            pass

        return output
    return wrapper


class ResultSet():
    """
    A class to hold the results of a tournament. Reads in a CSV file produced
    by the tournament class.
    """

    def __init__(self, filename,
                 players, repetitions,
                 processes=None, progress_bar=True):
        """
        Parameters
        ----------
            filename : string
                the file from which to read the interactions
            players : list
                A list of the names of players. If not known will be efficiently
                read from file.
            repetitions : int
                The number of repetitions of each match. If not know will be
                efficiently read from file.
            processes : integer
                The number of processes to be used for parallel processing
        """
        self.filename = filename
        self.players, self.repetitions = players, repetitions
        self.num_players = len(self.players)

        if progress_bar:
            self.progress_bar = tqdm.tqdm(total=25,
                                          desc="Analysing")

        df = dd.read_csv(filename)
        dask_tasks = self._build_tasks(df)

        if processes == 0:
            processes = cpu_count()

        out = self._compute_tasks(tasks=dask_tasks, processes=processes)

        self._reshape_out(out)

        if progress_bar:
            self.progress_bar.close()

    def _reshape_out(self, out):
        """
        Reshape the various pandas series objects to be of the required form and
        set the corresponding attributes.
        """

        (mean_per_reps_player_opponent_df,
         sum_per_player_opponent_df,
         sum_per_player_repetition_df,
         normalised_scores_series,
         initial_cooperation_count_series,
         interactions_count_series) = out

        self.payoffs = self._build_payoffs(mean_per_reps_player_opponent_df["Score per turn"])
        self.score_diffs = self._build_score_diffs(mean_per_reps_player_opponent_df["Score difference per turn"])
        self.match_lengths = self._build_match_lengths(mean_per_reps_player_opponent_df["Turns"])

        self.wins = self._build_wins(sum_per_player_repetition_df["Win"])
        self.scores = self._build_scores(sum_per_player_repetition_df["Score"])
        self.normalised_scores = self._build_normalised_scores(normalised_scores_series)
        self.cooperation = self._build_cooperation(sum_per_player_opponent_df["Cooperation count"])
        self.good_partner_matrix = self._build_good_partner_matrix(sum_per_player_opponent_df["Good partner"])

        columns = ["CC count", "CD count", "DC count", "DD count"]
        self.state_distribution = self._build_state_distribution(sum_per_player_opponent_df[columns])
        self.normalised_state_distribution = self._build_normalised_state_distribution()

        columns = ["CC to C count",
                   "CC to D count",
                   "CD to C count",
                   "CD to D count",
                   "DC to C count",
                   "DC to D count",
                   "DD to C count",
                   "DD to D count"]
        self.state_to_action_distribution = self._build_state_to_action_distribution(sum_per_player_opponent_df[columns])
        self.normalised_state_to_action_distribution = self._build_normalised_state_to_action_distribution()

        self.initial_cooperation_count = self._build_initial_cooperation_count(initial_cooperation_count_series)
        self.initial_cooperation_rate = self._build_initial_cooperation_rate(interactions_count_series)
        self.good_partner_rating = self._build_good_partner_rating(interactions_count_series)

        self.normalised_cooperation = self._build_normalised_cooperation()
        self.ranking = self._build_ranking()
        self.ranked_names = self._build_ranked_names()
        self.payoff_matrix = self._build_payoff_matrix()
        self.payoff_stddevs = self._build_payoff_stddevs()
        self.payoff_diffs_means = self._build_payoff_diffs_means()
        self.cooperating_rating = self._build_cooperating_rating()
        self.vengeful_cooperation = self._build_vengeful_cooperation()
        self.eigenjesus_rating = self._build_eigenjesus_rating()
        self.eigenmoses_rating = self._build_eigenmoses_rating()

    @update_progress_bar
    def _build_payoffs(self, payoffs_series):
        """
        Parameters
        ----------

            payoffs_series : pandas.Series

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
        payoffs_dict = dict(payoffs_series)
        payoffs = []
        for player_index in range(self.num_players):
            matrix = []
            for opponent_index in range(self.num_players):
                row = []
                for repetition in range(self.repetitions):
                    key = (repetition, player_index, opponent_index)
                    if key in payoffs_dict:
                        row.append(payoffs_dict[key])
                matrix.append(row)
            payoffs.append(matrix)
        return payoffs

    @update_progress_bar
    def _build_score_diffs(self, payoff_diffs_series):
        """
        Parameters
        ----------

            payoffs_diffs_series : pandas.Series

        Returns:
        --------
            The mean of per turn payoff differences
            List of the form:
            [ML1, ML2, ML3..., MLn]
            Where n is the number of players and MLi is a list of the form:
            [pi1, pi2, pi3, ..., pim]
            Where m is the number of players and pij is a list of the form:
            [uij1, uij2, ..., uijk]
            Where k is the number of repetitions and u is the mean utility
            difference (over all repetitions) obtained by player i against
            player j.
        """

        payoff_diffs_dict = payoff_diffs_series.to_dict()
        score_diffs = []
        for player_index in range(self.num_players):
            matrix = []
            for opponent_index in range(self.num_players):
                row = []
                for repetition in range(self.repetitions):
                    row.append(payoff_diffs_dict.get((repetition,
                                                      player_index,
                                                      opponent_index,
                                                      ), 0))
                matrix.append(row)
            score_diffs.append(matrix)
        return score_diffs

    @update_progress_bar
    def _build_match_lengths(self, length_series):
        length_dict = dict(length_series)
        match_lengths = []
        for repetition in range(self.repetitions):
            matrix = []
            for player_index in range(self.num_players):
                row = []
                for opponent_index in range(self.num_players):
                    row.append(length_dict.get((repetition,
                                                player_index,
                                                opponent_index), 0))
                matrix.append(row)
            match_lengths.append(matrix)
        return match_lengths

    @update_progress_bar
    def _build_wins(self, wins_series):
        wins_dict = wins_series.to_dict()
        wins = [[wins_dict.get((player_index, repetition), 0)
                  for repetition in range(self.repetitions)]
                 for player_index in range(self.num_players)]
        return wins

    @update_progress_bar
    def _build_scores(self, scores_series):
        scores_dict = scores_series.to_dict()
        scores = [[scores_series.get((player_index, repetition), 0)
                   for repetition in range(self.repetitions)]
                  for player_index in range(self.num_players)]
        return scores

    @update_progress_bar
    def _build_normalised_scores(self, normalised_scores_series):
        normalised_scores_dict = normalised_scores_series.to_dict()
        normalised_scores = [[normalised_scores_series.get((player_index,
                                                            repetition), 0)
                              for repetition in range(self.repetitions)]
                             for player_index in range(self.num_players)]
        return normalised_scores

    @update_progress_bar
    def _build_cooperation(self, cooperation_series):
        cooperation_dict = cooperation_series.to_dict()
        cooperation = []
        for player_index in range(self.num_players):
            row = []
            for opponent_index in range(self.num_players):
                count = cooperation_dict.get((player_index, opponent_index),0)
                if player_index == opponent_index:
					# Address double count
                    count = int(count / 2)
                row.append(count)
            cooperation.append(row)
        return cooperation

    @update_progress_bar
    def _build_good_partner_matrix(self, good_partner_series):
        good_partner_dict = dict(good_partner_series)
        good_partner_matrix = []
        for player_index in range(self.num_players):
            row = []
            for opponent_index in range(self.num_players):
                if player_index == opponent_index:
                    # The reduce operation implies a double count of self
                    # interactions.
                    row.append(0)
                else:
                    row.append(good_partner_dict.get((player_index,
                                                      opponent_index), 0))
            good_partner_matrix.append(row)
        return good_partner_matrix


    @update_progress_bar
    def _build_payoff_matrix(self):
        payoff_matrix = [[0 for opponent_index in range(self.num_players)]
                         for player_index in range(self.num_players)]

        pairs = itertools.product(range(self.num_players), repeat=2)

        for player_index, opponent_index in pairs:
            utilities = self.payoffs[player_index][opponent_index]
            if utilities:
                payoff_matrix[player_index][opponent_index] = mean(utilities)

        return payoff_matrix

    @update_progress_bar
    def _build_payoff_stddevs(self):
        payoff_stddevs = [[0 for opponent_index in range(self.num_players)]
                          for player_index in range(self.num_players)]

        pairs = itertools.product(range(self.num_players), repeat=2)

        for player_index, opponent_index in pairs:
            utilities = self.payoffs[player_index][opponent_index]
            if utilities:
                payoff_stddevs[player_index][opponent_index] = std(utilities)

        return payoff_stddevs


    @update_progress_bar
    def _build_payoff_diffs_means(self):
        payoff_diffs_means = [[mean(diff) for diff in player]
                               for player in self.score_diffs]

        return payoff_diffs_means

    @update_progress_bar
    def _build_state_distribution(self, state_distribution_series):
        state_key_map = {'CC count': (C, C),
                         'CD count': (C, D),
                         'DC count': (D, C),
                         'DD count': (D, D)}
        state_distribution = [[create_counter_dict(state_distribution_series,
                                                   player_index,
                                                   opponent_index,
                                                   state_key_map)
                               for opponent_index in range(self.num_players)]
                              for player_index in range(self.num_players)]
        return state_distribution

    @update_progress_bar
    def _build_normalised_state_distribution(self):
        """
        Returns:
        --------
            norm : list

            Normalised state distribution. A list of lists of counter objects:

            Dictionary where the keys are the states and the values are a
            normalized counts of the number of times that state occurs.
        """
        normalised_state_distribution = []
        for player in self.state_distribution:
            counters = []
            for counter in player:
                total = sum(counter.values())
                counters.append(Counter({key: value / total for
                                         key, value in counter.items()}))
            normalised_state_distribution.append(counters)
        return normalised_state_distribution

    @update_progress_bar
    def _build_state_to_action_distribution(self,
                                            state_to_action_distribution_series):
        state_to_action_key_map = {"CC to C count": ((C, C), C),
                                   "CC to D count": ((C, C), D),
                                   "CD to C count": ((C, D), C),
                                   "CD to D count": ((C, D), D),
                                   "DC to C count": ((D, C), C),
                                   "DC to D count": ((D, C), D),
                                   "DD to C count": ((D, D), C),
                                   "DD to D count": ((D, D), D)}
        state_to_action_distribution = [[
                create_counter_dict(state_to_action_distribution_series,
                                    player_index,
                                    opponent_index,
                                    state_to_action_key_map)
                                 for opponent_index in range(self.num_players)]
                                for player_index in range(self.num_players)]
        return state_to_action_distribution

    @update_progress_bar
    def _build_normalised_state_to_action_distribution(self):
        """
        Returns:
        --------
            norm : list

            A list of lists of counter objects.

            Dictionary where the keys are the states and the values are a
            normalized counts of the number of times that state goes to a given
            action.
        """
        normalised_state_to_action_distribution = []
        for player in self.state_to_action_distribution:
            counters = []
            for counter in player:
                norm_counter = Counter()
                for state in [(C, C), (C, D), (D, C), (D, D)]:
                    total = counter[(state, C)] + counter[(state, D)]
                    if total > 0:
                        for action in [C, D]:
                            if counter[(state, action)] > 0:
                                norm_counter[(state, action)] = counter[(state, action)] / total
                counters.append(norm_counter)
            normalised_state_to_action_distribution.append(counters)
        return normalised_state_to_action_distribution

    @update_progress_bar
    def _build_initial_cooperation_count(self, initial_cooperation_count_series):
        initial_cooperation_count_dict = initial_cooperation_count_series.to_dict()
        initial_cooperation_count = [
                initial_cooperation_count_dict.get(player_index, 0)
                                        for player_index in
                                        range(self.num_players)]
        return initial_cooperation_count

    @update_progress_bar
    def _build_normalised_cooperation(self):
        normalised_cooperation = [list(nan_to_num(row))
                                  for row in array(self.cooperation) /
                                  sum(map(array, self.match_lengths))]
        return normalised_cooperation

    @update_progress_bar
    def _build_initial_cooperation_rate(self, interactions_series):
        interactions_dict = interactions_series.to_dict()
        interactions_array = array([interactions_series.get(player_index, 0)
                                    for player_index in range(self.num_players)])
        initial_cooperation_rate = list(
           nan_to_num(array(self.initial_cooperation_count) /
                            interactions_array))
        return initial_cooperation_rate

    @update_progress_bar
    def _build_ranking(self):
        ranking = sorted(
                range(self.num_players),
                key=lambda i: -nanmedian(self.normalised_scores[i]))
        return ranking

    @update_progress_bar
    def _build_ranked_names(self):
        ranked_names = [str(self.players[i]) for i in self.ranking]
        return ranked_names

    @update_progress_bar
    def _build_eigenmoses_rating(self):
        """
        Returns:
        --------

        The eigenmoses rating as defined in:
        http://www.scottaaronson.com/morality.pdf
        """
        eigenvector, eigenvalue = eigen.principal_eigenvector(
            self.vengeful_cooperation)

        return eigenvector.tolist()

    @update_progress_bar
    def _build_eigenjesus_rating(self):
        """
        Returns:
        --------

        The eigenjesus rating as defined in:
        http://www.scottaaronson.com/morality.pdf
        """
        eigenvector, eigenvalue = eigen.principal_eigenvector(
            self.normalised_cooperation)

        return eigenvector.tolist()

    @update_progress_bar
    def _build_cooperating_rating(self):
        """
        Returns:
        --------

            The list of cooperation ratings
            List of the form:

            [ML1, ML2, ML3..., MLn]

            Where n is the number of players and MLi is a list of the form:

            [pi1, pi2, pi3, ..., pim]

            Where pij is the total number of cooperations divided by the total
            number of turns over all repetitions played by player i against
            player j.
        """

        plist = list(range(self.num_players))
        total_length_v_opponent = [zip(*[rep[player_index] for
                                         rep in self.match_lengths])
                                   for player_index in plist]
        lengths = [[sum(e) for j, e in enumerate(row) if i != j] for i, row in
                   enumerate(total_length_v_opponent)]

        cooperation = [[col for j, col in enumerate(row) if i != j]
                       for i, row in enumerate(self.cooperation)]
        # Max is to deal with edge cases of matches that have no turns
        cooperating_rating = [sum(cs) / max(1, sum(ls))
                              for cs, ls in zip(cooperation, lengths)]
        return cooperating_rating

    @update_progress_bar
    def _build_vengeful_cooperation(self):
        """
        Returns:
        --------

            The vengeful cooperation matrix derived from the
            normalised cooperation matrix:

                Dij = 2(Cij - 0.5)
        """
        vengeful_cooperation = [[2 * (element - 0.5) for element in row]
                                for row in self.normalised_cooperation]
        return vengeful_cooperation

    @update_progress_bar
    def _build_good_partner_rating(self, interactions_series):
        """
        At the end of a read of the data, build the good partner rating
        attribute
        """
        interactions_dict = interactions_series.to_dict()
        good_partner_rating = [sum(self.good_partner_matrix[player]) /
                               max(1, interactions_dict.get(player, 0))
                               for player in range(self.num_players)]
        return good_partner_rating

    def _compute_tasks(self, tasks, processes):
        """
        Compute all dask tasks
        """
        if processes is None:
            out = da.compute(*tasks, get=da.get)
        else:
            out = da.compute(*tasks, num_workers=processes)
        return out

    def _build_tasks(self, df):
        """
        Returns a tuple of dask tasks
        """
        groups = ["Repetition", "Player index", "Opponent index"]
        columns = ["Turns", "Score per turn", "Score difference per turn"]
        mean_per_reps_player_opponent_task = df.groupby(groups)[columns].mean()

        groups = ["Player index", "Opponent index"]
        columns = ["Cooperation count",
                   "CC count",
                   "CD count",
                   "DC count",
                   "DD count",
                   "CC to C count",
                   "CC to D count",
                   "CD to C count",
                   "CD to D count",
                   "DC to C count",
                   "DC to D count",
                   "DD to C count",
                   "DD to D count",
                   "Good partner"]
        sum_per_player_opponent_task = df.groupby(groups)[columns].sum()

        ignore_self_interactions_task = df["Player index"] != df["Opponent index"]
        adf = df[ignore_self_interactions_task]

        groups = ["Player index", "Repetition"]
        columns = ["Win", "Score"]
        sum_per_player_repetition_task = adf.groupby(groups)[columns].sum()

        normalised_scores_task = adf.groupby(["Player index",
                                              "Repetition"]
                                            )["Score per turn"].mean()
        initial_cooperation_count_task = adf.groupby(["Player index"])["Initial cooperation"].sum()
        interactions_count_task = adf.groupby("Player index")["Player index"].count()


        return (mean_per_reps_player_opponent_task,
                sum_per_player_opponent_task,
                sum_per_player_repetition_task,
                normalised_scores_task,
                initial_cooperation_count_task,
                interactions_count_task)

    def __eq__(self, other):
        """
        Check equality of results set

        Parameters
        ----------

            other : axelrod.ResultSet
                Another results set against which to check equality
        """
        return all([self.wins == other.wins,
                    self.match_lengths == other.match_lengths,
                    self.scores == other.scores,
                    self.normalised_scores == other.normalised_scores,
                    self.ranking == other.ranking,
                    self.ranked_names == other.ranked_names,
                    self.payoffs == other.payoffs,
                    self.payoff_matrix == other.payoff_matrix,
                    self.payoff_stddevs == other.payoff_stddevs,
                    self.score_diffs == other.score_diffs,
                    self.payoff_diffs_means == other.payoff_diffs_means,
                    self.cooperation == other.cooperation,
                    self.normalised_cooperation == other.normalised_cooperation,
                    self.vengeful_cooperation == other.vengeful_cooperation,
                    self.cooperating_rating == other.cooperating_rating,
                    self.good_partner_matrix == other.good_partner_matrix,
                    self.good_partner_rating == other.good_partner_rating,
                    self.eigenmoses_rating == other.eigenmoses_rating,
                    self.eigenjesus_rating == other.eigenjesus_rating])

    def __ne__(self, other):
        """
        Check inequality of results set

        Parameters
        ----------

            other : axelrod.ResultSet
                Another results set against which to check inequality
        """
        return not self.__eq__(other)

    def summarise(self):
        """
        Obtain summary of performance of each strategy:
        ordered by rank, including median normalised score and cooperation
        rating.

        Output
        ------

            A list of the form:

            [[player name, median score, cooperation_rating],...]

        """

        median_scores = map(nanmedian, self.normalised_scores)
        median_wins = map(nanmedian, self.wins)

        self.player = namedtuple("Player", ["Rank", "Name", "Median_score",
                                            "Cooperation_rating", "Wins",
                                            "Initial_C_rate", "CC_rate",
                                            "CD_rate", "DC_rate", "DD_rate",
                                            "CC_to_C_rate", "CD_to_C_rate",
                                            "DC_to_C_rate", "DD_to_C_rate"])

        states = [(C, C), (C, D), (D, C), (D, D)]
        state_prob = []
        for i, player in enumerate(self.normalised_state_distribution):
            counts = []
            for state in states:
                p = sum([opp[state] for j, opp in enumerate(player) if i != j])
                counts.append(p)
            try:
                counts = [c / sum(counts) for c in counts]
            except ZeroDivisionError:
                counts = [0 for c in counts]
            state_prob.append(counts)

        state_to_C_prob = []
        for player in self.normalised_state_to_action_distribution:
            rates = []
            for state in states:
                counts = [counter[(state, C)] for counter in player
                          if counter[(state, C)] > 0]

                if len(counts) > 0:
                    rate = mean(counts)
                else:
                    rate = 0

                rates.append(rate)
            state_to_C_prob.append(rates)

        summary_measures = list(zip(self.players, median_scores,
                                    self.cooperating_rating, median_wins,
                                    self.initial_cooperation_rate))

        summary_data = []
        for rank, i in enumerate(self.ranking):
            data = list(summary_measures[i]) + state_prob[i] + state_to_C_prob[i]
            summary_data.append(self.player(rank, *data))

        return summary_data

    def write_summary(self, filename):
        """
        Write a csv file containing summary data of the results of the form:

            "Rank", "Name", "Median-score-per-turn", "Cooperation-rating", "Initial_C_Rate", "Wins", "CC-Rate", "CD-Rate", "DC-Rate", "DD-rate","CC-to-C-Rate", "CD-to-C-Rate", "DC-to-C-Rate", "DD-to-C-rate"


        Parameters
        ----------
            filename : a filepath to which to write the data
        """
        summary_data = self.summarise()
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerow(self.player._fields)
            for player in summary_data:
                writer.writerow(player)


def create_counter_dict(df, player_index, opponent_index, key_map):
    """
    Create a Counter object mapping states (corresponding to columns of df) for
    players given by player_index, opponent_index. Renaming the variables with
    `key_map`. Used by `ResultSet._reshape_out`

    Parameters
    ----------
        df : a multiindex pandas df
        player_index: int
        opponent_index: int
        key_map : a dict
            maps cols of df to strings

    Returns
    -------
        A counter dictionary
    """
    counter = Counter()
    if player_index != opponent_index:
        if (player_index, opponent_index) in df.index:
            for key, value in df.loc[player_index, opponent_index].items():
                if value > 0:
                    counter[key_map[key]] = value
    return counter
