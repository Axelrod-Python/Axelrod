import unittest
import axelrod

from numpy import mean, std

from hypothesis import given
from hypothesis.strategies import floats, integers

class TestResultSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.players = (axelrod.Alternator(), axelrod.TitForTat(), axelrod.Defector())
        cls.turns = 5
        cls.matches = [
                       {
                        (0,1): axelrod.Match((cls.players[0], cls.players[1]),
                        turns=cls.turns),
                        (0,2): axelrod.Match((cls.players[0], cls.players[2]),
                        turns=cls.turns),
                        (1,2): axelrod.Match((cls.players[1], cls.players[2]),
                        turns=cls.turns)} for _ in range(3)
                        ]  # This would not actually be a round robin tournament
                           # (no cloned matches)

        for rep in cls.matches:
            for match in rep.values():
                match.play()

        cls.interactions = []
        for rep in cls.matches:
            cls.interactions.append({index_pair: match.result for
                                     index_pair, match in rep.items()})

        cls.expected_players_to_match_dicts = [{0: [rep[(0, 1)], rep[(0, 2)]],
                                                1: [rep[(0, 1)], rep[(1, 2)]],
                                                2: [rep[(1, 2)], rep[(0, 2)]]}
                                                for rep in cls.matches
                                              ]


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

        cls.expected_normalised_cooperation = [
                [0, mean([3 / 5.0 for _ in range(3)]), mean([3 / 5.0 for _ in range(3)])],
                [mean([3 / 5.0 for _ in range(3)]), 0, mean([1 / 5.0 for _ in range(3)])],
                [0, 0, 0],
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

        cls.expected_csv = (
            'Defector,Tit For Tat,Alternator\n2.6,1.7,1.5\n2.6,1.7,1.5\n2.6,1.7,1.5\n')

    def test_init(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.nplayers, len(self.players))
        self.assertEqual(rs.interactions, self.interactions)
        self.assertEqual(rs.nrepetitions, len(self.interactions))

        # Test structure of matches
        # This is really a test of the test
        for rep in rs.interactions:
            self.assertIsInstance(rep, dict)
            for index_pair, inter in rep.items():
                self.assertIsInstance(index_pair, tuple)
                self.assertIsInstance(inter, list)
                self.assertEqual(len(inter), self.turns)

    def test_null_results_matrix(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertEqual(
            rs._null_results_matrix, self.expected_null_results_matrix)

    def test_match_lengths(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.match_lengths, list)
        self.assertEqual(len(rs.match_lengths), rs.nrepetitions)
        self.assertEqual(rs.match_lengths, self.expected_match_lengths)

        #for rep in rs.match_lengths:
            #self.assertIsInstance(rep, list)
            #self.assertEqual(len(rep), len(self.players))

            #for i, opp in enumerate(rep):
                #self.assertIsInstance(opp, list)
                #self.assertEqual(len(opp), len(self.players))

                #for j, length in enumerate(opp):
                    #if i == j:  # Specific test for example match setup
                        #self.assertEqual(length, 0)
                    #else:
                        #self.assertEqual(length, self.turns)

    def test_scores(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.scores, list)
        self.assertEqual(len(rs.scores), rs.nplayers)
        self.assertEqual(rs.scores, self.expected_scores)

    def test_ranking(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.ranking, list)
        self.assertEqual(len(rs.ranking), rs.nplayers)
        self.assertEqual(rs.ranking, self.expected_ranking)

    def test_ranked_names(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.ranked_names, list)
        self.assertEqual(len(rs.ranked_names), rs.nplayers)
        self.assertEqual(rs.ranked_names, self.expected_ranked_names)

    def test_wins(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.wins, list)
        self.assertEqual(len(rs.wins), rs.nplayers)
        self.assertEqual(rs.wins, self.expected_wins)

    def test_normalised_scores(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.normalised_scores, list)
        self.assertEqual(len(rs.normalised_scores), rs.nplayers)
        self.assertEqual(rs.normalised_scores, self.expected_normalised_scores)

    def test_payoffs(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.payoffs, list)
        self.assertEqual(len(rs.payoffs), rs.nplayers)
        self.assertEqual(rs.payoffs, self.expected_payoffs)

    def test_payoff_matrix(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.payoff_matrix, list)
        self.assertEqual(len(rs.payoff_matrix), rs.nplayers)
        self.assertEqual(rs.payoff_matrix, self.expected_payoff_matrix)

    def test_score_diffs(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.score_diffs, list)
        self.assertEqual(len(rs.score_diffs), rs.nplayers)
        for i, row in enumerate(rs.score_diffs):
            for j, col in enumerate(row):
                for k, score in enumerate(col):
                    self.assertAlmostEqual(score,
                                     self.expected_score_diffs[i][j][k])

    def test_payoff_diffs_means(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.payoff_diffs_means, list)
        self.assertEqual(len(rs.payoff_diffs_means), rs.nplayers)
        for i, row in enumerate(rs.payoff_diffs_means):
            for j, col in enumerate(row):
                self.assertAlmostEqual(col,
                                 self.expected_payoff_diffs_means[i][j])

    def test_payoff_stddevs(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.payoff_stddevs, list)
        self.assertEqual(len(rs.payoff_stddevs), rs.nplayers)
        self.assertEqual(rs.payoff_stddevs, self.expected_payoff_stddevs)

    def test_cooperation(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.cooperation, list)
        self.assertEqual(len(rs.cooperation), rs.nplayers)
        self.assertEqual(rs.cooperation, self.expected_cooperation)

    def test_normalised_cooperation(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.normalised_cooperation, list)
        self.assertEqual(len(rs.normalised_cooperation), rs.nplayers)
        self.assertEqual(rs.normalised_cooperation,
                         self.expected_normalised_cooperation)

    def test_vengeful_cooperation(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.vengeful_cooperation, list)
        self.assertEqual(len(rs.vengeful_cooperation), rs.nplayers)
        self.assertEqual(rs.vengeful_cooperation,
                         self.expected_vengeful_cooperation)

    def test_cooperating_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.cooperating_rating, list)
        self.assertEqual(len(rs.cooperating_rating), rs.nplayers)
        self.assertEqual(rs.cooperating_rating,
                         self.expected_cooperating_rating)

    def test_good_partner_matrix(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.good_partner_matrix, list)
        self.assertEqual(len(rs.good_partner_matrix), rs.nplayers)
        self.assertEqual(rs.good_partner_matrix,
                         self.expected_good_partner_matrix)

    def test_good_partner_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.good_partner_rating, list)
        self.assertEqual(len(rs.good_partner_rating), rs.nplayers)
        self.assertEqual(rs.good_partner_rating,
                         self.expected_good_partner_rating)

    def test_eigenjesus_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.eigenjesus_rating, list)
        self.assertEqual(len(rs.eigenjesus_rating), rs.nplayers)
        for j, rate in enumerate(rs.eigenjesus_rating):
            self.assertAlmostEqual(rate, self.expected_eigenjesus_rating[j])

    def test_eigenmoses_rating(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertIsInstance(rs.eigenmoses_rating, list)
        self.assertEqual(len(rs.eigenmoses_rating), rs.nplayers)
        for j, rate in enumerate(rs.eigenmoses_rating):
            self.assertAlmostEqual(rate, self.expected_eigenmoses_rating[j])

    def test_csv(self):
        rs = axelrod.ResultSet(self.players, self.interactions)
        self.assertEqual(rs.csv(), self.expected_csv)
