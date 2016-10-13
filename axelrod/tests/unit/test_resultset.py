import unittest
import axelrod
import axelrod.interaction_utils as iu

from numpy import mean, std, nanmedian, nanmean

import csv
from collections import Counter

from hypothesis import given, settings
from axelrod.tests.property import tournaments, prob_end_tournaments


class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.filename = "test_outputs/test_results.csv"

        cls.players = [axelrod.Alternator(), axelrod.TitForTat(),
                       axelrod.Defector()]
        cls.turns = 5
        cls.matches = {
                        (0,1): [axelrod.Match((cls.players[0], cls.players[1]),
                        turns=cls.turns) for _ in range(3)],
                        (0,2): [axelrod.Match((cls.players[0], cls.players[2]),
                        turns=cls.turns) for _ in range(3)],
                        (1,2): [axelrod.Match((cls.players[1], cls.players[2]),
                        turns=cls.turns) for _ in range(3)]}
                          # This would not actually be a round robin tournament
                           # (no cloned matches)

        cls.interactions = {}
        for index_pair, matches in cls.matches.items():
            for match in matches:
                match.play()
                try:
                    cls.interactions[index_pair].append(match.result)
                except KeyError:
                    cls.interactions[index_pair] = [match.result]

        cls.expected_players_to_match_dicts = {0: cls.matches[(0, 1)] + cls.matches[(0, 2)],
                                               1: cls.matches[(0, 1)] + cls.matches[(1, 2)],
                                               2: cls.matches[(1, 2)] + cls.matches[(0, 2)]}

        cls.expected_match_lengths =[
               [[0, 5, 5], [5, 0, 5], [5, 5, 0]]
               for _ in range(3)
                ]

        cls.expected_scores =[
               [15, 15, 15],
               [17, 17, 17],
               [26, 26, 26]
                ]

        cls.expected_wins =[
               [0, 0, 0],
               [0, 0, 0],
               [2, 2, 2]
                ]

        cls.expected_normalised_scores =[
               [3.0 / 2 for _ in range(3)],
               [(13.0 / 5 + 4.0 / 5) / 2 for _ in range(3)],
               [(17.0 / 5 + 9.0 / 5) / 2 for _ in range(3)],
                ]

        cls.expected_ranking = [2, 1, 0]

        cls.expected_ranked_names = ['Defector', 'Tit For Tat', 'Alternator']

        cls.expected_null_results_matrix = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

        cls.expected_payoffs = [
            [[], [13/5.0 for _ in range(3)], [2/5.0 for _ in range(3)]],
            [[13/5.0 for _ in range(3)], [], [4/5.0 for _ in range(3)]],
            [[17/5.0 for _ in range(3)], [9/5.0 for _ in range(3)], []]
        ]

        norm_scores = cls.expected_normalised_scores
        cls.expected_score_diffs = [
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [-3.0, -3.0, -3.0]],
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [-1.0, -1.0, -1.0]],
            [[3.0, 3.0, 3.0],
             [1.0, 1.0, 1.0],
             [0.0, 0.0, 0.0]],
        ]

        cls.expected_payoff_diffs_means = [
            [0.0, 0.0, -3.0],
            [0.0, 0.0, -1.0],
            [3.0, 1.0, 0.0]
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [0, mean([13/5.0 for _ in range(3)]), mean([2/5.0 for _ in range(3)])],
            [mean([13/5.0 for _ in range(3)]), 0, mean([4/5.0 for _ in range(3)])],
            [mean([17/5.0 for _ in range(3)]), mean([9/5.0 for _ in range(3)]), 0]
        ]

        cls.expected_payoff_stddevs = [
            [0, std([13/5.0 for _ in range(3)]), std([2/5.0 for _ in range(3)])],
            [std([13/5.0 for _ in range(3)]), 0, std([4/5.0 for _ in range(3)])],
            [std([17/5.0 for _ in range(3)]), std([9/5.0 for _ in range(3)]), 0]
        ]

        cls.expected_cooperation = [
                [0, 9, 9],
                [9, 0, 3],
                [0, 0, 0],
            ]

        cls.expected_state_distribution = [
                [], [], []
            ]

        cls.expected_normalised_cooperation = [
                [0, mean([3 / 5.0 for _ in range(3)]), mean([3 / 5.0 for _ in range(3)])],
                [mean([3 / 5.0 for _ in range(3)]), 0, mean([1 / 5.0 for _ in range(3)])],
                [0, 0, 0],
            ]

        cls.expected_state_distribution = [
                [Counter(),
                 Counter({('D', 'C'): 6, ('C', 'D'): 6, ('C', 'C'): 3}),
                 Counter({('C', 'D'): 9, ('D', 'D'): 6})],
                [Counter({('D', 'C'): 6, ('C', 'D'): 6, ('C', 'C'): 3}),
                 Counter(),
                 Counter({('D', 'D'): 12, ('C', 'D'): 3})],
                [Counter({('D', 'C'): 9, ('D', 'D'): 6}),
                 Counter({('D', 'D'): 12, ('D', 'C'): 3}),
                 Counter()]
            ]

        cls.expected_normalised_state_distribution = [
                [Counter(),
                 Counter({('D', 'C'): 0.4, ('C', 'D'): 0.4, ('C', 'C'): 0.2}),
                 Counter({('C', 'D'): 0.6, ('D', 'D'): 0.4})],
                [Counter({('D', 'C'): 0.4, ('C', 'D'): 0.4, ('C', 'C'): 0.2}),
                 Counter(),
                 Counter({('D', 'D'): 0.8, ('C', 'D'): 0.2})],
                [Counter({('D', 'C'): 0.6, ('D', 'D'): 0.4}),
                 Counter({('D', 'D'): 0.8, ('D', 'C'): 0.2}),
                 Counter()]
            ]

        cls.expected_vengeful_cooperation = [[2 * element - 1 for element in row]
                                   for row in cls.expected_normalised_cooperation]

        cls.expected_cooperating_rating = [
                18.0 / 30,
                12.0 / 30,
                0
            ]

        cls.expected_good_partner_matrix = [
                [0, 3, 3],
                [3, 0, 3],
                [0, 0, 0]
            ]

        cls.expected_good_partner_rating = [
                1.0,
                1.0,
                0
            ]

        cls.expected_eigenjesus_rating = [
                0.5547001962252291,
                0.8320502943378436,
                0.0
            ]

        cls.expected_eigenmoses_rating = [
                -0.4578520302117101,
                0.7311328098872432,
                0.5057828909101213
            ]

    def test_init(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, len(self.players))
        self.assertEqual(rs.interactions, self.interactions)
        for inter in self.interactions.values():
            self.assertEqual(rs.repetitions, len(inter))

        # Test structure of matches
        # This is really a test of the test
        for index_pair, repetitions in rs.interactions.items():
            self.assertIsInstance(repetitions, list)
            self.assertIsInstance(index_pair, tuple)
            for interaction in repetitions:
                self.assertIsInstance(interaction, list)
                self.assertEqual(len(interaction), self.turns)

    def test_init_with_repetitions(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               repetitions=3,
                               progress_bar=False)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, len(self.players))
        self.assertEqual(rs.interactions, self.interactions)
        self.assertEqual(rs.repetitions, 3)

    def test_init_with_different_game(self):
        game = axelrod.Game(p=-1, r=-1, s=-1, t=-1)
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False, game=game)
        self.assertEqual(rs.game.RPST(), (-1, -1, -1, -1))

    def test_with_progress_bar(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertTrue(rs.progress_bar)
        self.assertEqual(rs.progress_bar.total, 10 + 2 * rs.nplayers)

        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=True)
        self.assertTrue(rs.progress_bar)
        self.assertEqual(rs.progress_bar.total, 10 + 2 * rs.nplayers)

    def test_match_lengths(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.match_lengths, list)
        self.assertEqual(len(rs.match_lengths), rs.repetitions)
        self.assertEqual(rs.match_lengths, self.expected_match_lengths)

        for rep in rs.match_lengths:
            self.assertIsInstance(rep, list)
            self.assertEqual(len(rep), len(self.players))

            for i, opp in enumerate(rep):
                self.assertIsInstance(opp, list)
                self.assertEqual(len(opp), len(self.players))

                for j, length in enumerate(opp):
                    if i == j:  # Specific test for example match setup
                        self.assertEqual(length, 0)
                    else:
                        self.assertEqual(length, self.turns)

    def test_scores(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.scores, list)
        self.assertEqual(len(rs.scores), rs.nplayers)
        self.assertEqual(rs.scores, self.expected_scores)

    def test_scores_with_different_game(self):
        game = axelrod.Game(p=-1, r=-1, s=-1, t=-1)
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False, game=game)
        for player in rs.scores:
            for score in player:
                self.assertFalse(score > 0)

    def test_ranking(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.ranking, list)
        self.assertEqual(len(rs.ranking), rs.nplayers)
        self.assertEqual(rs.ranking, self.expected_ranking)

    def test_ranked_names(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.ranked_names, list)
        self.assertEqual(len(rs.ranked_names), rs.nplayers)
        self.assertEqual(rs.ranked_names, self.expected_ranked_names)

    def test_wins(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.wins, list)
        self.assertEqual(len(rs.wins), rs.nplayers)
        self.assertEqual(rs.wins, self.expected_wins)

    def test_normalised_scores(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.normalised_scores, list)
        self.assertEqual(len(rs.normalised_scores), rs.nplayers)
        self.assertEqual(rs.normalised_scores, self.expected_normalised_scores)

    def test_payoffs(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.payoffs, list)
        self.assertEqual(len(rs.payoffs), rs.nplayers)
        self.assertEqual(rs.payoffs, self.expected_payoffs)

    def test_payoff_matrix(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.payoff_matrix, list)
        self.assertEqual(len(rs.payoff_matrix), rs.nplayers)
        self.assertEqual(rs.payoff_matrix, self.expected_payoff_matrix)

    def test_score_diffs(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.score_diffs, list)
        self.assertEqual(len(rs.score_diffs), rs.nplayers)
        for i, row in enumerate(rs.score_diffs):
            for j, col in enumerate(row):
                for k, score in enumerate(col):
                    self.assertAlmostEqual(score,
                                     self.expected_score_diffs[i][j][k])

    def test_payoff_diffs_means(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.payoff_diffs_means, list)
        self.assertEqual(len(rs.payoff_diffs_means), rs.nplayers)
        for i, row in enumerate(rs.payoff_diffs_means):
            for j, col in enumerate(row):
                self.assertAlmostEqual(col,
                                 self.expected_payoff_diffs_means[i][j])

    def test_payoff_stddevs(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.payoff_stddevs, list)
        self.assertEqual(len(rs.payoff_stddevs), rs.nplayers)
        self.assertEqual(rs.payoff_stddevs, self.expected_payoff_stddevs)

    def test_cooperation(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.cooperation, list)
        self.assertEqual(len(rs.cooperation), rs.nplayers)
        self.assertEqual(rs.cooperation, self.expected_cooperation)

    def test_normalised_cooperation(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.normalised_cooperation, list)
        self.assertEqual(len(rs.normalised_cooperation), rs.nplayers)
        self.assertEqual(rs.normalised_cooperation,
                         self.expected_normalised_cooperation)

    def test_state_distribution(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.state_distribution, list)
        self.assertEqual(len(rs.state_distribution), rs.nplayers)
        self.assertEqual(rs.state_distribution,
                         self.expected_state_distribution)

    def test_state_normalised_distribution(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.normalised_state_distribution, list)
        self.assertEqual(len(rs.normalised_state_distribution), rs.nplayers)
        self.assertEqual(rs.normalised_state_distribution,
                         self.expected_normalised_state_distribution)

    def test_vengeful_cooperation(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.vengeful_cooperation, list)
        self.assertEqual(len(rs.vengeful_cooperation), rs.nplayers)
        self.assertEqual(rs.vengeful_cooperation,
                         self.expected_vengeful_cooperation)

    def test_cooperating_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.cooperating_rating, list)
        self.assertEqual(len(rs.cooperating_rating), rs.nplayers)
        self.assertEqual(rs.cooperating_rating,
                         self.expected_cooperating_rating)

    def test_good_partner_matrix(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.good_partner_matrix, list)
        self.assertEqual(len(rs.good_partner_matrix), rs.nplayers)
        self.assertEqual(rs.good_partner_matrix,
                         self.expected_good_partner_matrix)

    def test_good_partner_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.good_partner_rating, list)
        self.assertEqual(len(rs.good_partner_rating), rs.nplayers)
        self.assertEqual(rs.good_partner_rating,
                         self.expected_good_partner_rating)

    def test_eigenjesus_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.eigenjesus_rating, list)
        self.assertEqual(len(rs.eigenjesus_rating), rs.nplayers)
        for j, rate in enumerate(rs.eigenjesus_rating):
            self.assertAlmostEqual(rate, self.expected_eigenjesus_rating[j])

    def test_eigenmoses_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.eigenmoses_rating, list)
        self.assertEqual(len(rs.eigenmoses_rating), rs.nplayers)
        for j, rate in enumerate(rs.eigenmoses_rating):
            self.assertAlmostEqual(rate, self.expected_eigenmoses_rating[j])

    def test_self_interaction_for_random_strategies(self):
        # Based on https://github.com/Axelrod-Python/Axelrod/issues/670
        axelrod.seed(0)
        players = [s() for s in axelrod.demo_strategies]
        tournament = axelrod.Tournament(players, repetitions=2, turns=5)
        results = tournament.play()
        self.assertEqual(results.payoff_diffs_means[-1][-1], 1.0)

    def test_equality(self):
        rs_sets = [axelrod.ResultSet(self.players, self.interactions,
                                     progress_bar=False) for _ in range(2)]
        self.assertEqual(rs_sets[0], rs_sets[1])

        players = [s() for s in axelrod.demo_strategies]
        tournament = axelrod.Tournament(players, repetitions=2, turns=5)
        results = tournament.play()
        self.assertNotEqual(results, rs_sets[0])

    def test_summarise(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        sd = rs.summarise()

        self.assertEqual(len(sd), len(rs.players))
        self.assertEqual([str(player.Name) for player in sd], rs.ranked_names)
        self.assertEqual([int(player.Rank) for player in sd],
                         list(range(len(self.players))))

        ranked_median_scores = [list(map(nanmedian, rs.normalised_scores))[i]
                                for i in rs.ranking]
        self.assertEqual([float(player.Median_score) for player in sd],
                         ranked_median_scores)

        ranked_cooperation_rating = [rs.cooperating_rating[i]
                                     for i in rs.ranking]
        self.assertEqual([float(player.Cooperation_rating) for player in sd],
                         ranked_cooperation_rating)

        ranked_median_wins = [nanmedian(rs.wins[i]) for i in rs.ranking]
        self.assertEqual([float(player.Wins) for player in sd],
                         ranked_median_wins)

        for player in sd:
            self.assertEqual(player.CC_rate + player.CD_rate + player.DC_rate + player.DD_rate, 1)

    def test_write_summary(self):
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        rs.write_summary(filename=self.filename)
        with open(self.filename, "r") as csvfile:
            ranked_names = []
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                ranked_names.append(row[1])
                self.assertEqual(len(row), 9)
        self.assertEqual(ranked_names[0], "Name")
        self.assertEqual(ranked_names[1:], rs.ranked_names)


class TestResultSetFromFile(unittest.TestCase):
    filename = "test_outputs/test_results_from_file.csv"
    players = [axelrod.Cooperator(),
               axelrod.TitForTat(),
               axelrod.Defector()]
    tournament = axelrod.Tournament(players=players, turns=2, repetitions=3)
    tournament.play(filename=filename)

    interactions = iu.read_interactions_from_file(filename)

    def test_init(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        self.assertEqual(brs.players, [str(p) for p in self.players])
        self.assertEqual(brs.nplayers, len(self.players))
        self.assertEqual(brs.repetitions, 3)

    def test_init_with_different_game(self):
        game = axelrod.Game(p=-1, r=-1, s=-1, t=-1)
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False,
                                   game=game)
        self.assertEqual(brs.game.RPST(), (-1, -1, -1, -1))

    def test_init_with_progress_bar(self):
        """Just able to test that no error occurs"""
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=True)
        self.assertEqual(brs.nplayers, len(self.players))
        self.assertEqual(brs.repetitions, 3)
        self.assertEqual(brs.num_interactions, 18)

    def test_init_with_num_interactions(self):
        """Just able to test that no error occurs"""
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=True,
                                        num_interactions=18)
        self.assertEqual(brs.nplayers, len(self.players))
        self.assertEqual(brs.repetitions, 3)
        self.assertEqual(brs.num_interactions, 18)

    def test_init_with_players_repetitions(self):
        """Just able to test that no error occurs"""
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=True,
                                        num_interactions=18, repetitions=3,
                                        players=[str(p) for p in self.players])
        self.assertEqual(brs.nplayers, len(self.players))
        self.assertEqual(brs.repetitions, 3)
        self.assertEqual(brs.num_interactions, 18)

    def test_equality(self):
        """A test that checks overall equality by comparing to the base result
        set class"""
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        rs = axelrod.ResultSet(self.players, self.interactions, progress_bar=False)
        self.assertEqual(rs, brs)

    def test_interactions_equality(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False,
                                        keep_interactions=True)
        rs = axelrod.ResultSet(self.players, self.interactions, progress_bar=False)
        self.assertEqual(rs.interactions, brs.interactions)

    @given(tournament=tournaments(max_size=5,
                                  max_turns=5,
                                  max_noise=0,
                                  max_repetitions=3))
    @settings(max_examples=50, timeout=0)
    def test_equality_with_round_robin(self, tournament):
        filename = "test_outputs/test_results.csv"
        tournament.play(filename=filename, progress_bar=False,
                        build_results=False)
        brs = axelrod.ResultSetFromFile(filename, progress_bar=False)
        interactions = iu.read_interactions_from_file(filename)
        rs = axelrod.ResultSet(tournament.players, interactions,
                               progress_bar=False)

        # Not testing full equality because of floating point errors.
        self.assertEqual(rs.scores, brs.scores)
        self.assertEqual(rs.wins, brs.wins)
        self.assertEqual(rs.match_lengths, brs.match_lengths)
        self.assertEqual(rs.cooperation, brs.cooperation)

        # Test that players are in the results (due to floating point errors
        # the order might not be the same)
        self.assertEqual(set(rs.ranked_names), set(brs.ranked_names))

    @given(tournament=prob_end_tournaments(max_size=5,
                                           min_prob_end=.7,
                                           max_repetitions=3))
    @settings(max_examples=50, timeout=0)
    def test_equality_with_prob_end(self, tournament):
        filename = "test_outputs/test_results.csv"
        tournament.play(filename=filename, progress_bar=False,
                        build_results=False)
        brs = axelrod.ResultSetFromFile(filename, progress_bar=False)
        interactions = iu.read_interactions_from_file(filename)
        rs = axelrod.ResultSet(tournament.players, interactions,
                               progress_bar=False)

        # Not testing full equality because of floating point errors.
        self.assertEqual(rs.ranked_names, brs.ranked_names)
        self.assertEqual(rs.scores, brs.scores)
        self.assertEqual(rs.match_lengths, brs.match_lengths)
        self.assertEqual(rs.cooperation, brs.cooperation)

    def test_read_players_and_repetitions(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        players, repetitions = brs._read_players_and_repetition_numbers()
        expected_players = ['Cooperator', 'Tit For Tat', 'Defector']
        self.assertEqual(brs.players, expected_players)
        self.assertEqual(repetitions, 3)

    def test_update_repetitions(self):
        brs = axelrod.ResultSetFromFile(filename=self.filename, progress_bar=False)
        brs.repetitions_d = {}
        brs._update_repetitions((0, 0))
        self.assertEqual(brs.repetitions_d, {(0, 0): 1})
        brs._update_repetitions((0, 0))
        self.assertEqual(brs.repetitions_d, {(0, 0): 2})
        brs._update_repetitions((0, 1))
        self.assertEqual(brs.repetitions_d, {(0, 0): 2, (0, 1): 1})

    def test_build_repetitions(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        brs.repetitions_d = {}
        brs._update_repetitions((0, 0))
        brs._update_repetitions((0, 0))
        repetitions = brs._build_repetitions()
        self.assertEqual(repetitions, 2)
        self.assertFalse(hasattr(brs, 'repetitions_d'))

    def test_update_players(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        brs.players_d = {}
        brs._update_players((0, 0), ('Cooperator', 'Cooperator'))
        self.assertEqual(brs.players_d, {0: 'Cooperator'})
        brs._update_players((0, 0), ('Cooperator', 'Cooperator'))
        self.assertEqual(brs.players_d, {0: 'Cooperator'})
        brs._update_players((0, 1), ('Cooperator', 'Defector'))
        self.assertEqual(brs.players_d, {0: 'Cooperator', 1: 'Defector'})

    def test_build_players(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        brs.players_d = {}
        brs._update_players((0, 0), ('Cooperator', 'Cooperator'))
        brs._update_players((0, 1), ('Cooperator', 'Defector'))
        players = brs._build_players()
        self.assertEqual(players, ['Cooperator', 'Defector'])
        self.assertFalse(hasattr(brs, 'players_d'))

    def test_build_read_match_chunks(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        matches = brs.read_match_chunks()
        chunk = next(matches)
        self.assertEqual(chunk[0],
                         ['0'] * 2 + ['Cooperator'] * 2 + [('C', 'C')] * 2)
        self.assertEqual(chunk[1],
                         ['0'] * 2 + ['Cooperator'] * 2 + [('C', 'C')] * 2)
        self.assertEqual(chunk[2],
                         ['0'] * 2 + ['Cooperator'] * 2 + [('C', 'C')] * 2)
        self.assertEqual(len(list(matches)), 5)

    def test_build_all(self):
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)

        brs._build_empty_metrics()
        self.assertNotEqual(brs, rs)
        brs._build_score_related_metrics(progress_bar=False)
        self.assertEqual(brs, rs)

    def test_buid_empty_metrics(self):
        plist = range(3)
        repetitions = 3
        replist = range(repetitions)
        expected_match_lengths = [[[0 for opponent in plist] for player in plist]
                                  for _ in replist]
        expected_wins = [[0 for _ in replist] for player in plist]
        expected_scores = [[0 for _ in replist] for player in plist]
        expected_normalised_scores = [[[] for _ in replist] for player in plist]
        expected_payoffs = [[[] for opponent in plist] for player in plist]
        expected_score_diffs = [[[0] * repetitions for opponent in plist]
                                for player in plist]
        expected_cooperation = [[0 for opponent in plist] for player in plist]
        expected_normalised_cooperation = [[[] for opponent in plist]
                                       for player in plist]
        expected_good_partner_matrix = [[0 for opponent in plist]
                                        for player in plist]

        expected_good_partner_rating = [0 for player in plist]
        brs = axelrod.ResultSetFromFile(self.filename, progress_bar=False)
        brs.match_lengths = []
        brs.wins = []
        brs.scores = []
        brs.normalised_scores = []
        brs.payoffs = []
        brs.score_diffs = []
        brs.cooperation = []
        brs.normalised_cooperation = []
        brs.good_partner_matrix = []
        brs.total_interactions = []
        brs.good_partner_rating = []
        brs._build_empty_metrics()
        self.assertEqual(brs.match_lengths, expected_match_lengths)
        self.assertEqual(brs.wins, expected_wins)
        self.assertEqual(brs.scores, expected_scores)
        self.assertEqual(brs.normalised_scores, expected_normalised_scores)
        self.assertEqual(brs.payoffs, expected_payoffs)
        self.assertEqual(brs.score_diffs, expected_score_diffs)
        self.assertEqual(brs.cooperation, expected_cooperation)
        self.assertEqual(brs.normalised_cooperation,
                         expected_normalised_cooperation)
        self.assertEqual(brs.good_partner_matrix, expected_good_partner_matrix)
        self.assertEqual(brs.good_partner_rating, expected_good_partner_rating)


class TestDecorator(unittest.TestCase):
    def test_update_progress_bar(self):
        method = lambda x: None
        self.assertEqual(axelrod.result_set.update_progress_bar(method)(1), None)


class TestResultSetSpatialStructure(TestResultSet):
    """
    Specific test for some spatial tournament.
    """
    @classmethod
    def setUpClass(cls):

        cls.players = [axelrod.Alternator(), axelrod.TitForTat(),
                       axelrod.Defector()]
        cls.turns = 5
        cls.edges = [(0, 1), (0, 2)]
        cls.matches = { (0,1): [axelrod.Match((cls.players[0], cls.players[1]),
                        turns=cls.turns) for _ in range(3)],
                        (0,2): [axelrod.Match((cls.players[0], cls.players[2]),
                        turns=cls.turns) for _ in range(3)]}

        cls.interactions = {}
        for index_pair, matches in cls.matches.items():
            for match in matches:
                match.play()
                try:
                    cls.interactions[index_pair].append(match.result)
                except KeyError:
                    cls.interactions[index_pair] = [match.result]

        cls.expected_players_to_match_dicts = {0: cls.matches[(0, 1)] + cls.matches[(0, 2)],
                                               1: cls.matches[(0, 1)] ,
                                               2: cls.matches[(0, 2)]}

        cls.expected_match_lengths =[
               [[0, 5, 5], [5, 0, 0], [5, 0, 0]]
               for _ in range(3)
                ]

        cls.expected_scores =[
               [15, 15, 15],
               [13, 13, 13],
               [17, 17, 17]
                ]

        cls.expected_wins =[
               [0, 0, 0],
               [0, 0, 0],
               [1, 1, 1]
                ]

        cls.expected_normalised_scores =[
               [3.0 / 2 for _ in range(3)],
               [(13.0 / 5 )  for _ in range(3)],
               [(17.0 / 5 )  for _ in range(3)],
                ]

        cls.expected_ranking = [2, 1, 0]

        cls.expected_ranked_names = ['Defector', 'Tit For Tat', 'Alternator']

        cls.expected_null_results_matrix = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

        cls.expected_payoffs = [
            [[], [13/5.0 for _ in range(3)], [2/5.0 for _ in range(3)]],
            [[13/5.0 for _ in range(3)], [], []],
            [[17/5.0 for _ in range(3)], [], []]
        ]

        norm_scores = cls.expected_normalised_scores
        cls.expected_score_diffs = [
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [-3.0, -3.0, -3.0]],
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]],
            [[3.0, 3.0, 3.0],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]],
        ]

        cls.expected_payoff_diffs_means = [
            [0.0, 0.0, -3.0],
            [0.0, 0.0, 0.0],
            [3.0, 0.0, 0.0]
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [0, mean([13/5.0 for _ in range(3)]), mean([2/5.0 for _ in range(3)])],
            [mean([13/5.0 for _ in range(3)]), 0, 0 ],
            [mean([17/5.0 for _ in range(3)]), 0 , 0]
        ]

        cls.expected_payoff_stddevs = [
            [0, std([13/5.0 for _ in range(3)]), std([2/5.0 for _ in range(3)])],
            [std([13/5.0 for _ in range(3)]), 0, 0 ],
            [std([17/5.0 for _ in range(3)]), 0, 0 ]
        ]

        cls.expected_cooperation = [
                [0, 9, 9],
                [9, 0, 0],
                [0, 0, 0],
            ]

        cls.expected_normalised_cooperation = [
            [0, mean([3 / 5.0 for _ in range(3)]), mean([3 / 5.0 for _ in range(3)])],
            [mean([3 / 5.0 for _ in range(3)]), 0, 0 ],
            [0, 0, 0],
            ]

        cls.expected_vengeful_cooperation = [[2 * element - 1 for element in row]
                                   for row in cls.expected_normalised_cooperation]

        cls.expected_cooperating_rating = [
                18.0 / 30,
                9.0 / 15,
                0
            ]

        cls.expected_good_partner_matrix = [
                [0, 3, 3],
                [3, 0, 0],
                [0, 0, 0]
            ]

        cls.expected_good_partner_rating = [
                1.0,
                1.0,
                0.0
            ]

        cls.expected_eigenjesus_rating = [
                0.447213595499958,
                0.894427190999916,
                0.0
            ]

        cls.expected_eigenmoses_rating = [
               -0.32929277996907086,
                0.7683498199278325,
                0.5488212999484519
            ]

        cls.expected_state_distribution = [
              [Counter(),
               Counter({('C', 'C'): 3, ('C', 'D'): 6, ('D', 'C'): 6}),
               Counter({('C', 'D'): 9, ('D', 'D'): 6})],
              [Counter({('C', 'C'): 3, ('C', 'D'): 6, ('D', 'C'): 6}),
               Counter(),
               Counter()],
              [Counter({('D', 'C'): 9, ('D', 'D'): 6}), Counter(), Counter()]
            ]

        cls.expected_normalised_state_distribution = [
              [Counter(),
               Counter({('C', 'C'): 0.2, ('C', 'D'): 0.4, ('D', 'C'): 0.4}),
               Counter({('C', 'D'): 0.6, ('D', 'D'): 0.4})],
              [Counter({('C', 'C'): 0.2, ('C', 'D'): 0.4, ('D', 'C'): 0.4}),
               Counter(),
               Counter()],
              [Counter({('D', 'C'): 0.6, ('D', 'D'): 0.4}), Counter(), Counter()]
            ]

        cls.expected_csv = (
            'Defector,Tit For Tat,Alternator\n3.4,2.6,1.5\n3.4,2.6,1.5\n3.4,2.6,1.5\n')

    def test_match_lengths(self):
        """
        Overwriting match lengths test. This method, among other things, checks
        that if two players interacted the length of that interaction equals the
        number of turns.

        Implementing this for the round robin tournament meant checking the
        interactions between each strategy and the rest strategies of the
        tournament.

        In a spatial tournament we need to check that: The length of interaction
        of players-nodes that are end vertices of an edge is equal to the
        number of turns. Otherwise it is 0.
        """
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        self.assertIsInstance(rs.match_lengths, list)
        self.assertEqual(len(rs.match_lengths), rs.repetitions)
        self.assertEqual(rs.match_lengths, self.expected_match_lengths)

        for rep in rs.match_lengths:
            self.assertIsInstance(rep, list)
            self.assertEqual(len(rep), len(self.players))

            for i, opp in enumerate(rep):
                self.assertIsInstance(opp, list)
                self.assertEqual(len(opp), len(self.players))

                for j, length in enumerate(opp):
                    edge = (i, j)
                    # Specific test for example match setup
                    if edge in self.edges or edge[::-1] in self.edges :
                        self.assertEqual(length, self.turns)
                    else:
                        self.assertEqual(length, 0)


class TestResultSetSpatialStructureTwo(TestResultSetSpatialStructure):

    @classmethod
    def setUpClass(cls):

        cls.players = [axelrod.Alternator(), axelrod.TitForTat(),
                       axelrod.Defector(), axelrod.Cooperator()]
        cls.turns = 5
        cls.edges = [(0, 1), (2, 3)]
        cls.matches = { (0,1): [axelrod.Match((cls.players[0], cls.players[1]),
                        turns=cls.turns) for _ in range(3)],
                        (2,3): [axelrod.Match((cls.players[2], cls.players[3]),
                        turns=cls.turns) for _ in range(3)]}

        cls.interactions = {}
        for index_pair, matches in cls.matches.items():
            for match in matches:
                match.play()
                try:
                    cls.interactions[index_pair].append(match.result)
                except KeyError:
                    cls.interactions[index_pair] = [match.result]

        cls.expected_players_to_match_dicts = {0: cls.matches[(0, 1)] ,
                                               1: cls.matches[(0, 1)] ,
                                               2: cls.matches[(2, 3)],
                                               3: cls.matches[(2, 3)]}

        cls.expected_match_lengths =[
               [[0, 5, 0, 0], [5, 0, 0, 0], [0, 0, 0, 5], [0, 0, 5, 0]]
               for _ in range(3)
                ]

        cls.expected_scores =[
               [ 13.0 for _ in range(3)],
               [ 13.0 for _ in range(3)],
               [ 25.0 for _ in range(3)],
               [ 0  for _ in range(3)]
                ]

        cls.expected_wins =[
               [0, 0, 0],
               [0, 0, 0],
               [1, 1, 1],
               [0, 0, 0]
                ]

        cls.expected_normalised_scores =[
               [(13.0 / 5 )  for _ in range(3)],
               [(13.0 / 5 )  for _ in range(3)],
               [(25.0 / 5 )  for _ in range(3)],
               [0  for _ in range(3)]
                ]

        cls.expected_ranking = [2, 0, 1, 3]

        cls.expected_ranked_names = ['Defector','Alternator',
                                     'Tit For Tat','Cooperator']

        cls.expected_null_results_matrix = [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ]

        cls.expected_payoffs = [
             [[], [13/5.0 for _ in range(3)], [], []],
             [[13/5.0 for _ in range(3)], [], [], []],
             [[], [], [], [25/5.0 for _ in range(3)]],
             [[], [], [0 for _ in range(3)], []]
        ]

        norm_scores = cls.expected_normalised_scores
        cls.expected_score_diffs = [
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [5.0, 5.0, 5.0]],
            [[0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0],
             [-5.0, -5.0, -5.0],
             [0.0, 0.0, 0.0]]
        ]

        cls.expected_payoff_diffs_means = [
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 5.0],
            [0.0, 0.0, -5.0, 0.0]
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [0, mean([13/5.0 for _ in range(3)]), 0, 0],
            [mean([13/5.0 for _ in range(3)]), 0, 0, 0],
            [0, 0, 0, mean([25/5.0 for _ in range(3)])],
            [0, 0, 0, 0]
        ]

        cls.expected_payoff_stddevs = [
            [0, std([13/5.0 for _ in range(3)]), 0, 0],
            [std([13/5.0 for _ in range(3)]), 0, 0, 0],
            [0, 0, 0, std([25/5.0 for _ in range(3)])],
            [0, 0, 0, 0]
        ]

        cls.expected_cooperation = [
                [0, 9, 0, 0],
                [9, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 15, 0]
            ]

        cls.expected_normalised_cooperation = [
                [0.0, mean([3 / 5.0 for _ in range(3)]), 0.0, 0.0],
                [mean([3 / 5.0 for _ in range(3)]), 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, mean([5 / 5.0 for _ in range(3)]), 0.0]
                ]

        cls.expected_vengeful_cooperation = [[2 * element - 1 for element in row]
                                   for row in cls.expected_normalised_cooperation]

        cls.expected_cooperating_rating = [
                18.0 / 30,
                18.0 / 30,
                0.0,
                30 / 30
            ]

        cls.expected_good_partner_matrix = [
                [0, 3, 0, 0],
                [3, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 3, 0]
            ]

        cls.expected_good_partner_rating = [
                1.0,
                1.0,
                0.0,
                1.0
            ]

        cls.expected_eigenjesus_rating = [
                0.7071067811865476,
                0.7071067811865476,
                0.0,
                0.0,
            ]

        cls.expected_eigenmoses_rating = [
                0.48505781033492573,
                0.48505781033492573,
                0.7090603855860735,
                0.1633132292825755
            ]

        cls.expected_state_distribution = [
               [Counter(),
                Counter({('C', 'C'): 3, ('C', 'D'): 6, ('D', 'C'): 6}),
                Counter(),
                Counter()],
               [Counter({('C', 'C'): 3, ('C', 'D'): 6, ('D', 'C'): 6}),
                Counter(),
                Counter(),
                Counter()],
               [Counter(), Counter(), Counter(), Counter({('D', 'C'): 15})],
               [Counter(), Counter(), Counter({('C', 'D'): 15}), Counter()]
            ]

        cls.expected_normalised_state_distribution = [
               [Counter(),
                Counter({('C', 'C'): 0.2, ('C', 'D'): 0.4, ('D', 'C'): 0.4}),
                Counter(),
                Counter()],
               [Counter({('C', 'C'): 0.2, ('C', 'D'): 0.4, ('D', 'C'): 0.4}),
                Counter(),
                Counter(),
                Counter()],
               [Counter(), Counter(), Counter(), Counter({('D', 'C'): 1.0})],
               [Counter(), Counter(), Counter({('C', 'D'): 1.0}), Counter()]
            ]

        cls.expected_csv = (
        "Defector,Alternator,Tit For Tat,Cooperator\n5.0,2.6,2.6,0.0\n5.0,2.6,2.6,0.0\n5.0,2.6,2.6,0.0\n")


class TestResultSetSpatialStructureThree(TestResultSetSpatialStructure):

    @classmethod
    def setUpClass(cls):

        cls.players = [axelrod.Alternator(), axelrod.TitForTat(),
                       axelrod.Defector(), axelrod.Cooperator()]
        cls.turns = 5
        cls.edges = [(0, 0), (1, 1), (2, 2), (3, 3)]
        cls.matches = {(i, i): [axelrod.Match((cls.players[i],
                                                cls.players[i].clone()),
                                                turns=cls.turns)
                        for _ in range(3)] for i in range(4)}

        cls.interactions = {}
        for index_pair, matches in cls.matches.items():
            for match in matches:
                match.play()

                try:
                    cls.interactions[index_pair].append(match.result)
                except KeyError:
                    cls.interactions[index_pair] = [match.result]

        cls.expected_players_to_match_dicts = {0: cls.matches[(0, 0)],
                                               1: cls.matches[(1, 1)],
                                               2: cls.matches[(2, 2)],
                                               3: cls.matches[(3, 3)]}

        cls.expected_match_lengths =[
               [[5, 0, 0, 0], [0, 5, 0, 0], [0, 0, 5, 0], [0, 0, 0, 5]]
               for _ in range(3)
                ]

        cls.expected_scores =[
            [0 for _ in range(3)] for _ in range(4)
                ]

        cls.expected_wins =[
            [0 for _ in range(3)] for _ in range(4)
                ]

        cls.expected_normalised_scores =[
               [0 for _ in range(3)] for i in range(4)
                ]

        cls.expected_ranking = [0, 1, 2, 3]

        cls.expected_ranked_names = ['Alternator','Tit For Tat','Defector','Cooperator']

        cls.expected_null_results_matrix = [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ]

        cls.expected_payoffs = [
             [[11 /5.0 for _ in range(3)], [], [], []],
             [[], [15 /5.0 for _ in range(3)], [], []],
             [[], [], [5 /5.0 for _ in range(3)], []],
             [[], [], [], [15 /5.0 for _ in range(3)]]
        ]

        norm_scores = cls.expected_normalised_scores
        cls.expected_score_diffs = [
            [[0.0 for _ in range(3)] for _ in range(4) ] for _ in range(4)
        ]

        cls.expected_payoff_diffs_means = [
            [0.0 for _ in range(4)] for _ in range(4)
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [mean([11/5.0 for _ in range(3)]),0, 0, 0],
            [0, mean([15/5.0 for _ in range(3)]), 0, 0],
            [0, 0, mean([5/5.0 for _ in range(3)]), 0],
            [0, 0, 0, mean([15/5.0 for _ in range(3)])]
        ]

        cls.expected_payoff_stddevs = [
            [std([11/5.0 for _ in range(3)]),0, 0, 0],
            [0, std([15/5.0 for _ in range(3)]), 0, 0],
            [0, 0, std([5/5.0 for _ in range(3)]), 0],
            [0, 0, 0, std([15/5.0 for _ in range(3)])]
        ]

        cls.expected_cooperation = [
            [0.0 for _ in range(4)] for _ in range(4)
            ]

        cls.expected_normalised_cooperation = [
                [mean([3 / 5.0 for _ in range(3)]), 0.0, 0.0, 0.0],
                [0.0, mean([5 / 5.0 for _ in range(3)]), 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, mean([5 / 5.0 for _ in range(3)])]
                ]

        cls.expected_vengeful_cooperation = [[2 * element - 1 for element in row]
                                   for row in cls.expected_normalised_cooperation]

        cls.expected_cooperating_rating = [
                0.0 for _ in range(4)
            ]

        cls.expected_good_partner_matrix = [
            [0.0 for _ in range(4)] for _ in range(4)
            ]

        cls.expected_good_partner_rating = [
                0.0 for _ in range(4)
            ]

        cls.expected_eigenjesus_rating = [
                0.0009235301367282831,
                0.7071064796379986,
                0.0,
                0.7071064796379986,
            ]

        cls.expected_eigenmoses_rating = [
                0.4765940316018446,
                0.3985944056208427,
                0.6746133178770147,
                0.3985944056208427
            ]

        cls.expected_state_distribution = [
                [Counter(), Counter(), Counter(), Counter()],
                [Counter(), Counter(), Counter(), Counter()],
                [Counter(), Counter(), Counter(), Counter()],
                [Counter(), Counter(), Counter(), Counter()]
            ]

        cls.expected_normalised_state_distribution = [
                [Counter(), Counter(), Counter(), Counter()],
                [Counter(), Counter(), Counter(), Counter()],
                [Counter(), Counter(), Counter(), Counter()],
                [Counter(), Counter(), Counter(), Counter()]
            ]


        cls.expected_csv = (
            'Alternator,Tit For Tat,Defector,Cooperator\nnan,nan,nan,nan\nnan,nan,nan,nan\nnan,nan,nan,nan\n')

    def test_equality(self):
        """Overwriting for this particular case"""
        pass

    def test_summarise(self):
        """Overwriting for this particular case"""
        rs = axelrod.ResultSet(self.players, self.interactions,
                               progress_bar=False)
        sd = rs.summarise()

        for player in sd:
            self.assertEqual(player.CC_rate, 0)
            self.assertEqual(player.CD_rate, 0)
            self.assertEqual(player.DC_rate, 0)
            self.assertEqual(player.DD_rate, 0)
