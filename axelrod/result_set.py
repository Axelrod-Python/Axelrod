from collections import namedtuple, Counter
import csv

from numpy import mean, nanmedian, std
import tqdm

from axelrod.actions import Actions
import axelrod.interaction_utils as iu
from . import eigen
from .game import Game


C, D = Actions.C, Actions.D


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


class ResultSet(object):
    """A class to hold the results of a tournament."""

    def __init__(self, players, interactions, repetitions=False,
                 progress_bar=True, game=None):
        """
        Parameters
        ----------
            players : list
                a list of player objects.
            interactions : list
                a list of dictionaries mapping tuples of player indices to
                interactions (1 for each repetition)
            repetitions : int
                The number of repetitions
            game : axlerod.game
                The particular game used.
            progress_bar : bool
                Whether or not to create a progress bar which will be updated
        """
        if game is None:
            self.game = Game()
        else:
            self.game = game

        self.interactions = interactions
        self.players = players
        self.num_matches = len(interactions)

        if not players or not repetitions:
            self.players, self.repetitions = self._read_players_and_repetition_numbers(progress_bar=progress_bar)
        else:
            self.players, self.repetitions = players, repetitions

        self.nplayers = len(self.players)

        self._build_empty_metrics()
        self._build_score_related_metrics(progress_bar=progress_bar)

    def create_progress_bar(self, desc=None):
        """
        Create a progress bar for a read through of the data file.

        Parameters
        ----------
            desc : string
                A description.
        """
        return tqdm.tqdm(total=self.num_matches, desc=desc)

    def _update_players(self, index_pair, players):
        """
        During a read of the data, update the internal players dictionary

        Parameters
        ----------

            index_pair : tuple
                A tuple of player indices
            players : tuple
                A tuple of player names
        """
        for index, player in zip(index_pair, players):
            if index not in self.players_d:
                self.players_d[index] = player

    def _update_repetitions(self, index_pair, nbr=1):
        """
        During a read of the data, update the internal repetitions dictionary

        Parameters
        ----------

            index_pair : tuple
                A tuple of player indices
            nbr : integer
                The number of repetitions
        """
        try:
            self.repetitions_d[index_pair] += nbr
        except KeyError:
            self.repetitions_d[index_pair] = nbr

    def _build_repetitions(self):
        """
        Count the number of repetitions

        Returns
        -------

            repetitions : int
                The number of repetitions
        """
        repetitions = max(self.repetitions_d.values())

        del self.repetitions_d  # Manual garbage collection
        return repetitions

    def _build_players(self):
        """
        List the players

        Returns
        -------

            players : list
                An ordered list of players
        """
        players = []
        for i in range(len(self.players_d)):
            players.append(self.players_d[i])

        del self.players_d  # Manual garbage collection
        return players

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

        plist = list(range(self.nplayers))
        total_length_v_opponent = [zip(*[rep[player_index] for
                                         rep in self.match_lengths])
                                   for player_index in plist]
        lengths = [[sum(e) for j, e in enumerate(row) if i != j] for i, row in
                   enumerate(total_length_v_opponent)]

        # Max is to deal with edge cases of matches that have no turns
        return [sum(cs) / max(1, sum(ls)) for cs, ls
                in zip(self.cooperation, lengths)]

    @update_progress_bar
    def _build_vengeful_cooperation(self):
        """
        Returns:
        --------

            The vengeful cooperation matrix derived from the
            normalised cooperation matrix:

                Dij = 2(Cij - 0.5)
        """
        return [[2 * (element - 0.5) for element in row]
                for row in self.normalised_cooperation]

    @update_progress_bar
    def _build_payoff_diffs_means(self):
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
        payoff_diffs_means = [[mean(diff) for diff in player]
                              for player in self.score_diffs]
        return payoff_diffs_means

    @update_progress_bar
    def _build_payoff_stddevs(self):
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

    @update_progress_bar
    def _build_payoff_matrix(self):
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

    @update_progress_bar
    def _build_ranked_names(self):
        """
        Returns:
        --------
            Returns the ranked names. A list of names as calculated by
            self.ranking.
        """

        return [str(self.players[i]) for i in self.ranking]

    @update_progress_bar
    def _build_ranking(self):
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
        norm = []
        for player in self.state_distribution:
            counters = []
            for counter in player:
                total = sum(counter.values())
                counters.append(Counter({key: value / total for
                                         key, value in counter.items()}))
            norm.append(counters)
        return norm

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
        norm = []
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
            norm.append(counters)
        return norm

    def _build_empty_metrics(self, keep_interactions=False):
        """
        Creates the various empty metrics ready to be updated as the data is
        read.

        Parameters
        ----------

            keep_interactions : bool
                Whether or not to load the interactions in to memory
        """
        plist = range(self.nplayers)
        replist = range(self.repetitions)
        self.match_lengths = [[[0 for opponent in plist] for player in plist]
                              for _ in replist]
        self.wins = [[0 for _ in replist] for player in plist]
        self.scores = [[0 for _ in replist] for player in plist]
        self.normalised_scores = [[[] for _ in replist] for player in plist]
        self.payoffs = [[[] for opponent in plist] for player in plist]
        self.score_diffs = [[[0] * self.repetitions for opponent in plist]
                            for player in plist]
        self.cooperation = [[0 for opponent in plist] for player in plist]
        self.normalised_cooperation = [[[] for opponent in plist]
                                       for player in plist]
        self.initial_cooperation_count = [0 for player in plist]
        self.state_distribution = [[Counter() for opponent in plist]
                                   for player in plist]
        self.state_to_action_distribution = [[Counter() for opponent in plist]
                                             for player in plist]
        self.good_partner_matrix = [[0 for opponent in plist]
                                    for player in plist]

        self.total_interactions = [0 for player in plist]
        self.good_partner_rating = [0 for player in plist]

        if keep_interactions:
            self.interactions = {}

    def _update_match_lengths(self, repetition, p1, p2, interaction):
        """
        During a read of the data, update the match lengths attribute

        Parameters
        ----------

            repetition : int
                The index of the repetition
            p1, p2 : int
                The indices of the first and second player
            interaction : list
                A list of tuples of interactions
        """
        self.match_lengths[repetition][p1][p2] = len(interaction)

    def _update_payoffs(self, p1, p2, scores_per_turn):
        """
        During a read of the data, update the payoffs attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            scores_per_turn : tuples
                A 2-tuple of the scores per turn for a given match
        """
        self.payoffs[p1][p2].append(scores_per_turn[0])
        if p1 != p2:
            self.payoffs[p2][p1].append(scores_per_turn[1])

    def _update_score_diffs(self, repetition, p1, p2, scores_per_turn):
        """
        During a read of the data, update the score diffs attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            scores_per_turn : tuples
                A 2-tuple of the scores per turn for a given match
        """
        diff = scores_per_turn[0] - scores_per_turn[1]
        self.score_diffs[p1][p2][repetition] = diff
        self.score_diffs[p2][p1][repetition] = -diff

    def _update_normalised_cooperation(self, p1, p2, interaction):
        """
        During a read of the data, update the normalised cooperation attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            interaction : list of tuples
                A list of interactions
        """
        normalised_cooperations = iu.compute_normalised_cooperation(interaction)

        self.normalised_cooperation[p1][p2].append(normalised_cooperations[0])
        self.normalised_cooperation[p2][p1].append(normalised_cooperations[1])

    def _update_wins(self, repetition, p1, p2, interaction):
        """
        During a read of the data, update the wins attribute

        Parameters
        ----------

            repetition : int
                The index of a repetition
            p1, p2 : int
                The indices of the first and second player
            interaction : list of tuples
                A list of interactions
        """
        match_winner_index = iu.compute_winner_index(interaction,
                                                     game=self.game)
        index_pair = [p1, p2]
        if match_winner_index is not False:
            winner_index = index_pair[match_winner_index]
            self.wins[winner_index][repetition] += 1

    def _update_scores(self, repetition, p1, p2, interaction):
        """
        During a read of the data, update the scores attribute

        Parameters
        ----------

            repetition : int
                The index of a repetition
            p1, p2 : int
                The indices of the first and second player
            interaction : list of tuples
                A list of interactions
        """
        final_scores = iu.compute_final_score(interaction, game=self.game)
        for index, player in enumerate([p1, p2]):
            player_score = final_scores[index]
            self.scores[player][repetition] += player_score

    def _update_normalised_scores(self, repetition, p1, p2, scores_per_turn):
        """
        During a read of the data, update the normalised scores attribute

        Parameters
        ----------

            repetition : int
                The index of a repetition
            p1, p2 : int
                The indices of the first and second player
            scores_per_turn : tuple
                A 2 tuple with the scores per turn of each player
        """
        for index, player in enumerate([p1, p2]):
            score_per_turn = scores_per_turn[index]
            self.normalised_scores[player][repetition].append(score_per_turn)

    def _update_cooperation(self, p1, p2, cooperations):
        """
        During a read of the data, update the cooperation attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            cooperations : tuple
                A 2 tuple with the count of cooperation each player
        """
        self.cooperation[p1][p2] += cooperations[0]
        self.cooperation[p2][p1] += cooperations[1]

    def _update_initial_cooperation_count(self, p1, p2, initial_cooperations):
        """
        During a read of the data, update the initial cooperation count
        attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            initial_cooperations : tuple
                A 2 tuple with a 0 or 1 indicating if the initial move of each
                player was Cooperation (0) or Defection (1), e.g. (0, 1) for a
                round (C, D)
        """
        self.initial_cooperation_count[p1] += initial_cooperations[0]
        self.initial_cooperation_count[p2] += initial_cooperations[1]

    def _update_state_distribution(self, p1, p2, counter):
        """
        During a read of the data, update the state_distribution attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            counter : collections.Counter
                A counter object for the states of a match
        """
        self.state_distribution[p1][p2] += counter

        counter[(C, D)], counter[(D, C)] = counter[(D, C)], counter[(C, D)]
        self.state_distribution[p2][p1] += counter

    def _update_state_to_action_distribution(self, p1, p2, counter_list):
        """
        During a read of the data, update the state_distribution attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            counter_list : list of collections.Counter
                A list of counter objects for the states to action of a match
        """
        counter = counter_list[0]
        self.state_to_action_distribution[p1][p2] += counter

        counter = counter_list[1]
        for act in [C, D]:
            counter[((C, D), act)], counter[((D, C), act)] = counter[((D, C), act)], counter[((C, D), act)]
        self.state_to_action_distribution[p2][p1] += counter

    def _update_good_partner_matrix(self, p1, p2, cooperations):
        """
        During a read of the data, update the good partner matrix attribute

        Parameters
        ----------

            p1, p2 : int
                The indices of the first and second player
            cooperations : tuple
                A 2 tuple with the count of cooperation each player
        """
        if cooperations[0] >= cooperations[1]:
            self.good_partner_matrix[p1][p2] += 1
        if cooperations[1] >= cooperations[0]:
            self.good_partner_matrix[p2][p1] += 1

    def _summarise_normalised_scores(self):
        """
        At the end of a read of the data, finalise the normalised scores
        """
        for i, rep in enumerate(self.normalised_scores):
            for j, player_scores in enumerate(rep):
                if player_scores != []:
                    self.normalised_scores[i][j] = mean(player_scores)
                else:
                    self.normalised_scores[i][j] = 0
            try:
                self.progress_bar.update()
            except AttributeError:
                pass

    def _summarise_normalised_cooperation(self):
        """
        At the end of a read of the data, finalise the normalised cooperation
        """
        for i, rep in enumerate(self.normalised_cooperation):
            for j, cooperation in enumerate(rep):
                if cooperation != []:
                    self.normalised_cooperation[i][j] = mean(cooperation)
                else:
                    self.normalised_cooperation[i][j] = 0
            try:
                self.progress_bar.update()
            except AttributeError:
                pass

    @update_progress_bar
    def _build_good_partner_rating(self):
        """
        At the end of a read of the data, build the good partner rating
        attribute
        """
        return [sum(self.good_partner_matrix[player]) /
                max(1, self.total_interactions[player])
                for player in range(self.nplayers)]

    @update_progress_bar
    def _build_initial_cooperation_rate(self):
        """
        At the end of a read of the data, build the normalised initial
        cooperation rate attribute
        """
        return [self.initial_cooperation_count[player] /
                max(1, self.total_interactions[player])
                for player in range(self.nplayers)]

    def _build_score_related_metrics(self, progress_bar=False,
                                     keep_interactions=False):
        """
        Read the data and carry out all relevant calculations.

        Parameters
        ----------
            progress_bar : bool
                Whether or not to display a progress bar
            keep_interactions : bool
                Whether or not to lad the interactions in to memory
        """
        match_chunks = self.read_match_chunks(progress_bar)

        for match in match_chunks:
            p1, p2 = int(match[0][0]), int(match[0][1])

            for repetition, record in enumerate(match):
                interaction = record[4:]

                if keep_interactions:
                    try:
                        self.interactions[(p1, p2)].append(interaction)
                    except KeyError:
                        self.interactions[(p1, p2)] = [interaction]

                scores_per_turn = iu.compute_final_score_per_turn(interaction,
                                                                 game=self.game)
                cooperations = iu.compute_cooperations(interaction)
                state_counter = iu.compute_state_distribution(interaction)

                self._update_match_lengths(repetition, p1, p2, interaction)
                self._update_payoffs(p1, p2, scores_per_turn)
                self._update_score_diffs(repetition, p1, p2, scores_per_turn)
                self._update_normalised_cooperation(p1, p2, interaction)

                if p1 != p2:  # Anything that ignores self interactions
                    state_to_actions = iu.compute_state_to_action_distribution(interaction)

                    for player in [p1, p2]:
                        self.total_interactions[player] += 1

                    self._update_match_lengths(repetition, p2, p1, interaction)
                    self._update_wins(repetition, p1, p2, interaction)
                    self._update_scores(repetition, p1, p2, interaction)
                    self._update_normalised_scores(repetition, p1, p2,
                                                   scores_per_turn)
                    self._update_cooperation(p1, p2, cooperations)
                    initial_coops = iu.compute_cooperations(interaction[:1])
                    self._update_initial_cooperation_count(p1, p2,
                                                           initial_coops)
                    self._update_state_distribution(p1, p2, state_counter)
                    self._update_state_to_action_distribution(p1, p2,
                                                              state_to_actions)
                    self._update_good_partner_matrix(p1, p2, cooperations)

        if progress_bar:
            self.progress_bar = tqdm.tqdm(total=13 + 2 * self.nplayers,
                                          desc="Finishing")
        self._summarise_normalised_scores()
        self._summarise_normalised_cooperation()

        self.ranking = self._build_ranking()
        self.normalised_state_distribution = self._build_normalised_state_distribution()
        self.normalised_state_to_action_distribution = self._build_normalised_state_to_action_distribution()
        self.ranked_names = self._build_ranked_names()
        self.payoff_matrix = self._build_payoff_matrix()
        self.payoff_stddevs = self._build_payoff_stddevs()
        self.payoff_diffs_means = self._build_payoff_diffs_means()
        self.vengeful_cooperation = self._build_vengeful_cooperation()
        self.cooperating_rating = self._build_cooperating_rating()
        self.initial_cooperation_rate = self._build_initial_cooperation_rate()
        self.good_partner_rating = self._build_good_partner_rating()
        self.eigenjesus_rating = self._build_eigenjesus_rating()
        self.eigenmoses_rating = self._build_eigenmoses_rating()

        if progress_bar:
            self.progress_bar.close()

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
                counts = [counter[(state, 'C')] for counter in player
                          if counter[(state, 'C')] > 0]

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

    def read_match_chunks(self, progress_bar=False):
        """
        A generator to return a given repetitions of matches

        Parameters
        ----------

            progress_bar : bool
                whether or not to display a progress bar

        Yields
        ------
            repetitions : list
                A list of lists include index pairs, player pairs and
                repetitions. All repetitions for a given pair are yielded
                together.
        """

        if progress_bar:
            progress_bar = self.create_progress_bar(desc="Analysing")

        for match_pair, interactions in self.interactions.items():
            players_pair = [self.players[i] for i in match_pair]
            repetitions = [list(match_pair) + players_pair + rep for rep in
                           interactions]
            if progress_bar:
                progress_bar.update()
            yield repetitions

        if progress_bar:
            progress_bar.close()

    def _read_players_and_repetition_numbers(self, progress_bar=False):
        """
        Read the players and the repetitions numbers

        Parameters
        ----------
            progress_bar : bool
                Whether or not to display a progress bar
        """

        if progress_bar:
            progress_bar = self.create_progress_bar(desc="Counting")

        self.players_d = {}
        self.repetitions_d = {}
        for index_pair, interactions in self.interactions.items():
            players = [self.players[i] for i in index_pair]
            self._update_repetitions(index_pair, len(interactions))
            self._update_players(index_pair, players)
            if progress_bar:
                progress_bar.update()

        if progress_bar:
            progress_bar.close()

        repetitions = self._build_repetitions()
        players = self._build_players()

        return players, repetitions


class ResultSetFromFile(ResultSet):
    """
    A class to hold the results of a tournament. Reads in a CSV file produced
    by the tournament class.
    """

    def __init__(self, filename, progress_bar=True,
                 num_interactions=False, players=False, repetitions=False,
                 game=None, keep_interactions=False):
        """
        Parameters
        ----------
            filename : string
                the file from which to read the interactions
            progress_bar : bool
                Whether or not to create a progress bar which will be updated
            num_interactions : int
                The number of interactions in the file. Used for the progress
                bar. If not known but progress_bar is true, will be efficiently
                read from file.
            players : list
                A list of the names of players. If not known will be efficiently
                read from file.
            repetitions : int
                The number of repetitions of each match. If not know will be
                efficiently read from file.
            game : axelrod.Game
                The particular game that should be used to calculate the scores.
            keep_interactions : bool
                Whether or not to load the interactions in to memory. WARNING:
                for large tournaments this drastically increases the memory
                required.
        """
        if game is None:
            self.game = Game()
        else:
            self.game = game

        self.filename = filename
        self.num_interactions = num_interactions

        if not players and not repetitions:
            self.players, self.repetitions = self._read_players_and_repetition_numbers(progress_bar=progress_bar)
        else:
            self.players, self.repetitions = players, repetitions
        self.nplayers = len(self.players)

        self._build_empty_metrics(keep_interactions=keep_interactions)
        self._build_score_related_metrics(progress_bar=progress_bar,
                                          keep_interactions=keep_interactions)

    def create_progress_bar(self, desc=None):
        """
        Create a progress bar for a read through of the data file.

        Parameters
        ----------
            desc : string
                A description.
        """
        if not self.num_interactions:
            with open(self.filename) as f:
                self.num_interactions = sum(1 for line in f)
        return tqdm.tqdm(total=self.num_interactions, desc=desc)

    def _read_players_and_repetition_numbers(self, progress_bar=False):
        """
        Read the players and the repetitions numbers

        Parameters
        ----------
            progress_bar : bool
                Whether or not to display a progress bar
        """

        if progress_bar:
            progress_bar = self.create_progress_bar(desc="Counting")

        self.players_d = {}
        self.repetitions_d = {}
        with open(self.filename, 'r') as f:
            for row in csv.reader(f):
                index_pair = (int(row[0]), int(row[1]))
                players = (row[2], row[3])
                self._update_repetitions(index_pair)
                self._update_players(index_pair, players)
                if progress_bar:
                    progress_bar.update()

        if progress_bar:
            progress_bar.close()

        repetitions = self._build_repetitions()
        players = self._build_players()

        return players, repetitions

    def read_match_chunks(self, progress_bar=False):
        """
        A generator to return a given repetitions of matches

        Parameters
        ----------

            progress_bar : bool
                whether or not to display a progress bar

        Yields
        ------
            repetitions : list
                A list of lists include index pairs, player pairs and
                repetitions. All repetitions for a given pair are yielded
                together.
        """

        if progress_bar:
            progress_bar = self.create_progress_bar(desc="Analysing")

        with open(self.filename, 'r') as f:
            csv_reader = csv.reader(f)
            repetitions = []
            count = 0
            for row in csv_reader:
                index_and_names = row[:4]
                interactions = list(zip(row[4], row[5]))
                repetitions.append(index_and_names + interactions)
                count += 1
                if progress_bar:
                    progress_bar.update()
                if count == self.repetitions:
                    yield repetitions
                    repetitions = []
                    count = 0

        if progress_bar:
            progress_bar.close()
