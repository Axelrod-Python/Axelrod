import csv
import pathlib
import unittest
from collections import Counter

import pandas as pd
from dask.dataframe.core import DataFrame
from hypothesis import given, settings
from numpy import mean, nanmedian, std

import axelrod as axl
from axelrod.load_data_ import axl_filename
from axelrod.result_set import create_counter_dict
from axelrod.tests.property import prob_end_tournaments, tournaments

C, D = axl.Action.C, axl.Action.D


class TestResultSet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        path = pathlib.Path("test_outputs/test_results.csv")
        cls.filename = str(axl_filename(path))

        cls.players = [axl.Alternator(), axl.TitForTat(), axl.Defector()]
        cls.repetitions = 3
        cls.turns = 5
        cls.edges = [(0, 1), (0, 2), (1, 2)]

        cls.expected_match_lengths = [
            [[0, 5, 5], [5, 0, 5], [5, 5, 0]] for _ in range(3)
        ]

        cls.expected_scores = [[15, 15, 15], [17, 17, 17], [26, 26, 26]]

        cls.expected_wins = [[0, 0, 0], [0, 0, 0], [2, 2, 2]]

        cls.expected_normalised_scores = [
            [3 / 2 for _ in range(3)],
            [(13 / 5 + 4 / 5) / 2 for _ in range(3)],
            [(17 / 5 + 9 / 5) / 2 for _ in range(3)],
        ]

        cls.expected_ranking = [2, 1, 0]

        cls.expected_ranked_names = ["Defector", "Tit For Tat", "Alternator"]

        cls.expected_null_results_matrix = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

        cls.expected_payoffs = [
            [[], [13 / 5 for _ in range(3)], [2 / 5 for _ in range(3)]],
            [[13 / 5 for _ in range(3)], [], [4 / 5 for _ in range(3)]],
            [[17 / 5 for _ in range(3)], [9 / 5 for _ in range(3)], []],
        ]

        cls.expected_score_diffs = [
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [-3.0, -3.0, -3.0]],
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [-1.0, -1.0, -1.0]],
            [[3.0, 3.0, 3.0], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0]],
        ]

        cls.expected_payoff_diffs_means = [
            [0.0, 0.0, -3.0],
            [0.0, 0.0, -1.0],
            [3.0, 1.0, 0.0],
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [
                0,
                mean([13 / 5 for _ in range(3)]),
                mean([2 / 5 for _ in range(3)]),
            ],
            [
                mean([13 / 5 for _ in range(3)]),
                0,
                mean([4 / 5 for _ in range(3)]),
            ],
            [
                mean([17 / 5 for _ in range(3)]),
                mean([9 / 5 for _ in range(3)]),
                0,
            ],
        ]

        cls.expected_payoff_stddevs = [
            [
                0,
                std([13 / 5 for _ in range(3)]),
                std([2 / 5 for _ in range(3)]),
            ],
            [
                std([13 / 5 for _ in range(3)]),
                0,
                std([4 / 5 for _ in range(3)]),
            ],
            [
                std([17 / 5 for _ in range(3)]),
                std([9 / 5 for _ in range(3)]),
                0,
            ],
        ]

        cls.expected_cooperation = [[0, 9, 9], [9, 0, 3], [0, 0, 0]]

        cls.expected_initial_cooperation_count = [6, 6, 0]
        cls.expected_initial_cooperation_rate = [1, 1, 0]

        cls.expected_normalised_cooperation = [
            [
                0,
                mean([3 / 5 for _ in range(3)]),
                mean([3 / 5 for _ in range(3)]),
            ],
            [
                mean([3 / 5 for _ in range(3)]),
                0,
                mean([1 / 5 for _ in range(3)]),
            ],
            [0, 0, 0],
        ]

        cls.expected_state_distribution = [
            [
                Counter(),
                Counter({(D, C): 6, (C, D): 6, (C, C): 3}),
                Counter({(C, D): 9, (D, D): 6}),
            ],
            [
                Counter({(D, C): 6, (C, D): 6, (C, C): 3}),
                Counter(),
                Counter({(D, D): 12, (C, D): 3}),
            ],
            [
                Counter({(D, C): 9, (D, D): 6}),
                Counter({(D, D): 12, (D, C): 3}),
                Counter(),
            ],
        ]

        cls.expected_normalised_state_distribution = [
            [
                Counter(),
                Counter({(D, C): 0.4, (C, D): 0.4, (C, C): 0.2}),
                Counter({(C, D): 0.6, (D, D): 0.4}),
            ],
            [
                Counter({(D, C): 0.4, (C, D): 0.4, (C, C): 0.2}),
                Counter(),
                Counter({(D, D): 0.8, (C, D): 0.2}),
            ],
            [
                Counter({(D, C): 0.6, (D, D): 0.4}),
                Counter({(D, D): 0.8, (D, C): 0.2}),
                Counter(),
            ],
        ]

        cls.expected_state_to_action_distribution = [
            [
                Counter(),
                Counter({((C, C), D): 3, ((C, D), D): 3, ((D, C), C): 6}),
                Counter({((C, D), D): 6, ((D, D), C): 6}),
            ],
            [
                Counter({((C, C), C): 3, ((D, C), C): 3, ((C, D), D): 6}),
                Counter(),
                Counter({((C, D), D): 3, ((D, D), D): 9}),
            ],
            [
                Counter({((D, C), D): 6, ((D, D), D): 6}),
                Counter({((D, C), D): 3, ((D, D), D): 9}),
                Counter(),
            ],
        ]

        cls.expected_normalised_state_to_action_distribution = [
            [
                Counter(),
                Counter({((C, C), D): 1, ((C, D), D): 1, ((D, C), C): 1}),
                Counter({((C, D), D): 1, ((D, D), C): 1}),
            ],
            [
                Counter({((C, C), C): 1, ((D, C), C): 1, ((C, D), D): 1}),
                Counter(),
                Counter({((C, D), D): 1, ((D, D), D): 1}),
            ],
            [
                Counter({((D, C), D): 1, ((D, D), D): 1}),
                Counter({((D, C), D): 1, ((D, D), D): 1}),
                Counter(),
            ],
        ]

        cls.expected_vengeful_cooperation = [
            [2 * element - 1 for element in row]
            for row in cls.expected_normalised_cooperation
        ]

        cls.expected_cooperating_rating = [18 / 30, 12 / 30, 0]

        cls.expected_good_partner_matrix = [[0, 3, 3], [3, 0, 3], [0, 0, 0]]

        cls.expected_good_partner_rating = [1.0, 1.0, 0]

        cls.expected_eigenjesus_rating = [
            0.5547001962252291,
            0.8320502943378436,
            0.0,
        ]

        cls.expected_eigenmoses_rating = [
            -0.4578520302117101,
            0.7311328098872432,
            0.5057828909101213,
        ]

    def test_init(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.num_players, len(self.players))

    def _clear_matrix(self, matrix):
        for i, row in enumerate(matrix):
            for j, _ in enumerate(row):
                matrix[i][j] = 0

    def test_ne_vectors(self):
        rs_1 = axl.ResultSet(self.filename, self.players, self.repetitions)

        rs_2 = axl.ResultSet(self.filename, self.players, self.repetitions)

        # A different vector
        rs_2.eigenmoses_rating = (-1, -1, -1)

        self.assertNotEqual(rs_1, rs_2)

    def test_nan_vectors(self):
        rs_1 = axl.ResultSet(self.filename, self.players, self.repetitions)
        # Force a broken eigenmoses, by replacing vengeful_cooperation with
        # zeroes.
        self._clear_matrix(rs_1.vengeful_cooperation)
        rs_1.eigenmoses_rating = rs_1._build_eigenmoses_rating()

        rs_2 = axl.ResultSet(self.filename, self.players, self.repetitions)
        # Force a broken eigenmoses, by replacing vengeful_cooperation with
        # zeroes.
        self._clear_matrix(rs_2.vengeful_cooperation)
        rs_2.eigenmoses_rating = rs_2._build_eigenmoses_rating()

        self.assertEqual(rs_1, rs_2)

    def test_init_multiprocessing(self):
        rs = axl.ResultSet(
            self.filename,
            self.players,
            self.repetitions,
            progress_bar=False,
            processes=2,
        )
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.num_players, len(self.players))

        rs = axl.ResultSet(
            self.filename,
            self.players,
            self.repetitions,
            progress_bar=False,
            processes=0,
        )
        self.assertEqual(rs.players, self.players)
        self.assertEqual(rs.num_players, len(self.players))

    def test_with_progress_bar(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=True
        )
        self.assertTrue(rs.progress_bar)
        self.assertEqual(rs.progress_bar.total, 25)
        self.assertEqual(rs.progress_bar.n, rs.progress_bar.total)

    def test_match_lengths(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
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
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.scores, list)
        self.assertEqual(len(rs.scores), rs.num_players)
        self.assertEqual(rs.scores, self.expected_scores)

    def test_ranking(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.ranking, list)
        self.assertEqual(len(rs.ranking), rs.num_players)
        self.assertEqual(rs.ranking, self.expected_ranking)

    def test_ranked_names(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.ranked_names, list)
        self.assertEqual(len(rs.ranked_names), rs.num_players)
        self.assertEqual(rs.ranked_names, self.expected_ranked_names)

    def test_wins(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.wins, list)
        self.assertEqual(len(rs.wins), rs.num_players)
        self.assertEqual(rs.wins, self.expected_wins)

    def test_normalised_scores(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.normalised_scores, list)
        self.assertEqual(len(rs.normalised_scores), rs.num_players)
        self.assertEqual(rs.normalised_scores, self.expected_normalised_scores)

    def test_payoffs(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.payoffs, list)
        self.assertEqual(len(rs.payoffs), rs.num_players)
        self.assertEqual(rs.payoffs, self.expected_payoffs)

    def test_payoff_matrix(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.payoff_matrix, list)
        self.assertEqual(len(rs.payoff_matrix), rs.num_players)
        self.assertEqual(rs.payoff_matrix, self.expected_payoff_matrix)

    def test_score_diffs(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.score_diffs, list)
        self.assertEqual(len(rs.score_diffs), rs.num_players)
        for i, row in enumerate(rs.score_diffs):
            for j, col in enumerate(row):
                for k, score in enumerate(col):
                    self.assertAlmostEqual(
                        score, self.expected_score_diffs[i][j][k]
                    )

    def test_payoff_diffs_means(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.payoff_diffs_means, list)
        self.assertEqual(len(rs.payoff_diffs_means), rs.num_players)
        for i, row in enumerate(rs.payoff_diffs_means):
            for j, col in enumerate(row):
                self.assertAlmostEqual(
                    col, self.expected_payoff_diffs_means[i][j]
                )

    def test_payoff_stddevs(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.payoff_stddevs, list)
        self.assertEqual(len(rs.payoff_stddevs), rs.num_players)
        self.assertEqual(rs.payoff_stddevs, self.expected_payoff_stddevs)

    def test_cooperation(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.cooperation, list)
        self.assertEqual(len(rs.cooperation), rs.num_players)
        self.assertEqual(rs.cooperation, self.expected_cooperation)

    def test_initial_cooperation_count(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.initial_cooperation_count, list)
        self.assertEqual(len(rs.initial_cooperation_count), rs.num_players)
        self.assertEqual(
            rs.initial_cooperation_count,
            self.expected_initial_cooperation_count,
        )

    def test_normalised_cooperation(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.normalised_cooperation, list)
        self.assertEqual(len(rs.normalised_cooperation), rs.num_players)
        for i, row in enumerate(rs.normalised_cooperation):
            for j, col in enumerate(row):
                self.assertAlmostEqual(
                    col, self.expected_normalised_cooperation[i][j]
                )

    def test_initial_cooperation_rate(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.initial_cooperation_rate, list)
        self.assertEqual(len(rs.initial_cooperation_rate), rs.num_players)
        self.assertEqual(
            rs.initial_cooperation_rate, self.expected_initial_cooperation_rate
        )

    def test_state_distribution(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.state_distribution, list)
        self.assertEqual(len(rs.state_distribution), rs.num_players)
        self.assertEqual(
            rs.state_distribution, self.expected_state_distribution
        )

    def test_state_normalised_distribution(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.normalised_state_distribution, list)
        self.assertEqual(len(rs.normalised_state_distribution), rs.num_players)
        self.assertEqual(
            rs.normalised_state_distribution,
            self.expected_normalised_state_distribution,
        )

    def test_state_to_action_distribution(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.state_to_action_distribution, list)
        self.assertEqual(len(rs.state_to_action_distribution), rs.num_players)
        self.assertEqual(
            rs.state_to_action_distribution[1],
            self.expected_state_to_action_distribution[1],
        )

    def test_normalised_state_to_action_distribution(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.normalised_state_to_action_distribution, list)
        self.assertEqual(
            len(rs.normalised_state_to_action_distribution), rs.num_players
        )
        self.assertEqual(
            rs.normalised_state_to_action_distribution,
            self.expected_normalised_state_to_action_distribution,
        )

    def test_vengeful_cooperation(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.vengeful_cooperation, list)
        self.assertEqual(len(rs.vengeful_cooperation), rs.num_players)
        for i, row in enumerate(rs.vengeful_cooperation):
            for j, col in enumerate(row):
                self.assertAlmostEqual(
                    col, self.expected_vengeful_cooperation[i][j]
                )

    def test_cooperating_rating(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.cooperating_rating, list)
        self.assertEqual(len(rs.cooperating_rating), rs.num_players)
        self.assertEqual(
            rs.cooperating_rating, self.expected_cooperating_rating
        )

    def test_good_partner_matrix(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.good_partner_matrix, list)
        self.assertEqual(len(rs.good_partner_matrix), rs.num_players)
        self.assertEqual(
            rs.good_partner_matrix, self.expected_good_partner_matrix
        )

    def test_good_partner_rating(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.good_partner_rating, list)
        self.assertEqual(len(rs.good_partner_rating), rs.num_players)
        self.assertEqual(
            rs.good_partner_rating, self.expected_good_partner_rating
        )

    def test_eigenjesus_rating(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.eigenjesus_rating, list)
        self.assertEqual(len(rs.eigenjesus_rating), rs.num_players)
        for j, rate in enumerate(rs.eigenjesus_rating):
            self.assertAlmostEqual(rate, self.expected_eigenjesus_rating[j])

    def test_eigenmoses_rating(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        self.assertIsInstance(rs.eigenmoses_rating, list)
        self.assertEqual(len(rs.eigenmoses_rating), rs.num_players)
        for j, rate in enumerate(rs.eigenmoses_rating):
            self.assertAlmostEqual(rate, self.expected_eigenmoses_rating[j])

    def test_self_interaction_for_random_strategies(self):
        # Based on https://github.com/Axelrod-Python/Axelrod/issues/670
        # Note that the conclusion of #670 is incorrect and only includes one of
        # the copies of the strategy.
        players = [s() for s in axl.demo_strategies]
        tournament = axl.Tournament(players, repetitions=2, turns=5, seed=0)
        results = tournament.play(progress_bar=False)
        self.assertEqual(results.payoff_diffs_means[-1][-1], 0.0)

    def test_equality(self):
        rs_sets = [
            axl.ResultSet(
                self.filename,
                self.players,
                self.repetitions,
                progress_bar=False,
            )
            for _ in range(2)
        ]
        self.assertEqual(rs_sets[0], rs_sets[1])

        players = [s() for s in axl.demo_strategies]
        tournament = axl.Tournament(players, repetitions=2, turns=5)
        results = tournament.play(progress_bar=False)
        self.assertNotEqual(results, rs_sets[0])

    def test_summarise(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        sd = rs.summarise()

        self.assertEqual(len(sd), len(rs.players))
        self.assertEqual([str(player.Name) for player in sd], rs.ranked_names)
        self.assertEqual(
            [int(player.Rank) for player in sd], list(range(len(self.players)))
        )

        ranked_median_scores = [
            list(map(nanmedian, rs.normalised_scores))[i] for i in rs.ranking
        ]
        self.assertEqual(
            [float(player.Median_score) for player in sd], ranked_median_scores
        )

        ranked_cooperation_rating = [
            rs.cooperating_rating[i] for i in rs.ranking
        ]
        self.assertEqual(
            [float(player.Cooperation_rating) for player in sd],
            ranked_cooperation_rating,
        )

        ranked_median_wins = [nanmedian(rs.wins[i]) for i in rs.ranking]
        self.assertEqual(
            [float(player.Wins) for player in sd], ranked_median_wins
        )

        ranked_initial_coop_rates = [
            self.expected_initial_cooperation_rate[i] for i in rs.ranking
        ]
        self.assertEqual(
            [float(player.Initial_C_rate) for player in sd],
            ranked_initial_coop_rates,
        )

        for player in sd:
            self.assertEqual(
                player.CC_rate
                + player.CD_rate
                + player.DC_rate
                + player.DD_rate,
                1,
            )
            for rate in [
                player.CC_to_C_rate,
                player.CD_to_C_rate,
                player.DC_to_C_rate,
                player.DD_to_C_rate,
            ]:
                self.assertLessEqual(rate, 1)
                self.assertGreaterEqual(rate, 0)

    # When converting Action to Enum, test coverage gap exposed from example in
    # docs/tutorial/getting_started/summarising_tournaments.rst
    def test_summarise_regression_test(self):
        players = [
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
            axl.Grudger(),
        ]
        tournament = axl.Tournament(players, turns=10, repetitions=3)
        results = tournament.play()

        summary = [
            (
                0,
                "Defector",
                2.6000000000000001,
                0.0,
                3.0,
                0.0,
                0.0,
                0.0,
                0.4000000000000001,
                0.6,
                0,
                0,
                0,
                0,
            ),
            (
                1,
                "Tit For Tat",
                2.3000000000000003,
                0.7,
                0.0,
                1.0,
                0.6666666666666666,
                0.03333333333333333,
                0.0,
                0.3,
                1.0,
                0,
                0,
                0,
            ),
            (
                2,
                "Grudger",
                2.3000000000000003,
                0.7,
                0.0,
                1.0,
                0.6666666666666666,
                0.03333333333333333,
                0.0,
                0.3,
                1.0,
                0,
                0,
                0,
            ),
            (
                3,
                "Cooperator",
                2.0,
                1.0,
                0.0,
                1.0,
                0.6666666666666666,
                0.3333333333333333,
                0.0,
                0.0,
                1.0,
                1.0,
                0,
                0,
            ),
        ]
        for outer_index, player in enumerate(results.summarise()):
            for inner_index, value in enumerate(player):
                if isinstance(value, str):
                    self.assertEqual(value, summary[outer_index][inner_index])
                else:
                    self.assertAlmostEqual(
                        value, summary[outer_index][inner_index], places=3
                    )

    def test_write_summary(self):
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        rs.write_summary(filename=self.filename + ".summary")
        with open(self.filename + ".summary", "r") as csvfile:
            ranked_names = []
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                ranked_names.append(row[1])
                self.assertEqual(len(row), 14)
        self.assertEqual(ranked_names[0], "Name")
        self.assertEqual(ranked_names[1:], rs.ranked_names)


class TestDecorator(unittest.TestCase):
    def test_update_progress_bar(self):
        method = lambda x: None
        self.assertEqual(axl.result_set.update_progress_bar(method)(1), None)


class TestResultSetSpatialStructure(TestResultSet):
    """
    Specific test for some spatial tournament.
    """

    @classmethod
    def setUpClass(cls):

        path = pathlib.Path("test_outputs/test_results_spatial.csv")
        cls.filename = str(axl_filename(path))
        cls.players = [axl.Alternator(), axl.TitForTat(), axl.Defector()]
        cls.turns = 5
        cls.repetitions = 3
        cls.edges = [(0, 1), (0, 2)]

        cls.expected_match_lengths = [
            [[0, 5, 5], [5, 0, 0], [5, 0, 0]] for _ in range(3)
        ]

        cls.expected_scores = [[15, 15, 15], [13, 13, 13], [17, 17, 17]]

        cls.expected_wins = [[0, 0, 0], [0, 0, 0], [1, 1, 1]]

        cls.expected_normalised_scores = [
            [3 / 2 for _ in range(3)],
            [(13 / 5) for _ in range(3)],
            [(17 / 5) for _ in range(3)],
        ]

        cls.expected_ranking = [2, 1, 0]

        cls.expected_ranked_names = ["Defector", "Tit For Tat", "Alternator"]

        cls.expected_null_results_matrix = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        ]

        cls.expected_payoffs = [
            [[], [13 / 5 for _ in range(3)], [2 / 5 for _ in range(3)]],
            [[13 / 5 for _ in range(3)], [], []],
            [[17 / 5 for _ in range(3)], [], []],
        ]

        cls.expected_score_diffs = [
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [-3.0, -3.0, -3.0]],
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[3.0, 3.0, 3.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        ]

        cls.expected_payoff_diffs_means = [
            [0.0, 0.0, -3.0],
            [0.0, 0.0, 0.0],
            [3.0, 0.0, 0.0],
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [
                0,
                mean([13 / 5 for _ in range(3)]),
                mean([2 / 5 for _ in range(3)]),
            ],
            [mean([13 / 5 for _ in range(3)]), 0, 0],
            [mean([17 / 5 for _ in range(3)]), 0, 0],
        ]

        cls.expected_payoff_stddevs = [
            [
                0,
                std([13 / 5 for _ in range(3)]),
                std([2 / 5 for _ in range(3)]),
            ],
            [std([13 / 5 for _ in range(3)]), 0, 0],
            [std([17 / 5 for _ in range(3)]), 0, 0],
        ]

        cls.expected_cooperation = [[0, 9, 9], [9, 0, 0], [0, 0, 0]]

        cls.expected_normalised_cooperation = [
            [
                0,
                mean([3 / 5 for _ in range(3)]),
                mean([3 / 5 for _ in range(3)]),
            ],
            [mean([3 / 5 for _ in range(3)]), 0, 0],
            [0, 0, 0],
        ]

        cls.expected_initial_cooperation_count = [6, 3, 0]
        cls.expected_initial_cooperation_rate = [1, 1, 0]

        cls.expected_vengeful_cooperation = [
            [2 * element - 1 for element in row]
            for row in cls.expected_normalised_cooperation
        ]

        cls.expected_cooperating_rating = [18 / 30, 9 / 15, 0]

        cls.expected_good_partner_matrix = [[0, 3, 3], [3, 0, 0], [0, 0, 0]]

        cls.expected_good_partner_rating = [1.0, 1.0, 0.0]

        cls.expected_eigenjesus_rating = [
            0.447213595499958,
            0.894427190999916,
            0.0,
        ]

        cls.expected_eigenmoses_rating = [
            -0.32929277996907086,
            0.7683498199278325,
            0.5488212999484519,
        ]

        cls.expected_state_distribution = [
            [
                Counter(),
                Counter({(C, C): 3, (C, D): 6, (D, C): 6}),
                Counter({(C, D): 9, (D, D): 6}),
            ],
            [Counter({(C, C): 3, (C, D): 6, (D, C): 6}), Counter(), Counter()],
            [Counter({(D, C): 9, (D, D): 6}), Counter(), Counter()],
        ]

        cls.expected_normalised_state_distribution = [
            [
                Counter(),
                Counter({(C, C): 0.2, (C, D): 0.4, (D, C): 0.4}),
                Counter({(C, D): 0.6, (D, D): 0.4}),
            ],
            [
                Counter({(C, C): 0.2, (C, D): 0.4, (D, C): 0.4}),
                Counter(),
                Counter(),
            ],
            [Counter({(D, C): 0.6, (D, D): 0.4}), Counter(), Counter()],
        ]

        cls.expected_state_to_action_distribution = [
            [
                Counter(),
                Counter({((C, C), D): 3, ((C, D), D): 3, ((D, C), C): 6}),
                Counter({((C, D), D): 6, ((D, D), C): 6}),
            ],
            [
                Counter({((C, C), C): 3, ((D, C), C): 3, ((C, D), D): 6}),
                Counter(),
                Counter(),
            ],
            [Counter({((D, C), D): 6, ((D, D), D): 6}), Counter(), Counter()],
        ]

        cls.expected_normalised_state_to_action_distribution = [
            [
                Counter(),
                Counter({((C, C), D): 1.0, ((C, D), D): 1.0, ((D, C), C): 1.0}),
                Counter({((C, D), D): 1.0, ((D, D), C): 1.0}),
            ],
            [
                Counter({((C, C), C): 1.0, ((D, C), C): 1.0, ((C, D), D): 1.0}),
                Counter(),
                Counter(),
            ],
            [
                Counter({((D, C), D): 1.0, ((D, D), D): 1.0}),
                Counter(),
                Counter(),
            ],
        ]

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
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
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
                    if edge in self.edges or edge[::-1] in self.edges:
                        self.assertEqual(length, self.turns)
                    else:
                        self.assertEqual(length, 0)


class TestResultSetSpatialStructureTwo(TestResultSetSpatialStructure):
    @classmethod
    def setUpClass(cls):

        path = pathlib.Path("test_outputs/test_results_spatial_two.csv")
        cls.filename = str(axl_filename(path))
        cls.players = [
            axl.Alternator(),
            axl.TitForTat(),
            axl.Defector(),
            axl.Cooperator(),
        ]
        cls.turns = 5
        cls.repetitions = 3
        cls.edges = [(0, 1), (2, 3)]

        cls.expected_match_lengths = [
            [[0, 5, 0, 0], [5, 0, 0, 0], [0, 0, 0, 5], [0, 0, 5, 0]]
            for _ in range(3)
        ]

        cls.expected_scores = [
            [13.0 for _ in range(3)],
            [13.0 for _ in range(3)],
            [25.0 for _ in range(3)],
            [0 for _ in range(3)],
        ]

        cls.expected_wins = [[0, 0, 0], [0, 0, 0], [1, 1, 1], [0, 0, 0]]

        cls.expected_normalised_scores = [
            [(13 / 5) for _ in range(3)],
            [(13 / 5) for _ in range(3)],
            [(25 / 5) for _ in range(3)],
            [0 for _ in range(3)],
        ]

        cls.expected_ranking = [2, 0, 1, 3]

        cls.expected_ranked_names = [
            "Defector",
            "Alternator",
            "Tit For Tat",
            "Cooperator",
        ]

        cls.expected_null_results_matrix = [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ]

        cls.expected_payoffs = [
            [[], [13 / 5 for _ in range(3)], [], []],
            [[13 / 5 for _ in range(3)], [], [], []],
            [[], [], [], [25 / 5 for _ in range(3)]],
            [[], [], [0 for _ in range(3)], []],
        ]

        cls.expected_score_diffs = [
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [5.0, 5.0, 5.0],
            ],
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [-5.0, -5.0, -5.0],
                [0.0, 0.0, 0.0],
            ],
        ]

        cls.expected_payoff_diffs_means = [
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 5.0],
            [0.0, 0.0, -5.0, 0.0],
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [0, mean([13 / 5 for _ in range(3)]), 0, 0],
            [mean([13 / 5 for _ in range(3)]), 0, 0, 0],
            [0, 0, 0, mean([25 / 5 for _ in range(3)])],
            [0, 0, 0, 0],
        ]

        cls.expected_payoff_stddevs = [
            [0, std([13 / 5 for _ in range(3)]), 0, 0],
            [std([13 / 5 for _ in range(3)]), 0, 0, 0],
            [0, 0, 0, std([25 / 5 for _ in range(3)])],
            [0, 0, 0, 0],
        ]

        cls.expected_cooperation = [
            [0, 9, 0, 0],
            [9, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 15, 0],
        ]

        cls.expected_normalised_cooperation = [
            [0.0, mean([3 / 5 for _ in range(3)]), 0.0, 0.0],
            [mean([3 / 5 for _ in range(3)]), 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, mean([5 / 5 for _ in range(3)]), 0.0],
        ]

        cls.expected_initial_cooperation_count = [3.0, 3.0, 0, 3.0]
        cls.expected_initial_cooperation_rate = [1.0, 1.0, 0, 1.0]

        cls.expected_vengeful_cooperation = [
            [2 * element - 1 for element in row]
            for row in cls.expected_normalised_cooperation
        ]

        cls.expected_cooperating_rating = [18 / 30, 18 / 30, 0.0, 30 / 30]

        cls.expected_good_partner_matrix = [
            [0, 3, 0, 0],
            [3, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 3, 0],
        ]

        cls.expected_good_partner_rating = [1.0, 1.0, 0.0, 1.0]

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
            0.1633132292825755,
        ]

        cls.expected_state_distribution = [
            [
                Counter(),
                Counter({(C, C): 3, (C, D): 6, (D, C): 6}),
                Counter(),
                Counter(),
            ],
            [
                Counter({(C, C): 3, (C, D): 6, (D, C): 6}),
                Counter(),
                Counter(),
                Counter(),
            ],
            [Counter(), Counter(), Counter(), Counter({(D, C): 15})],
            [Counter(), Counter(), Counter({(C, D): 15}), Counter()],
        ]

        cls.expected_normalised_state_distribution = [
            [
                Counter(),
                Counter({(C, C): 0.2, (C, D): 0.4, (D, C): 0.4}),
                Counter(),
                Counter(),
            ],
            [
                Counter({(C, C): 0.2, (C, D): 0.4, (D, C): 0.4}),
                Counter(),
                Counter(),
                Counter(),
            ],
            [Counter(), Counter(), Counter(), Counter({(D, C): 1.0})],
            [Counter(), Counter(), Counter({(C, D): 1.0}), Counter()],
        ]

        cls.expected_state_to_action_distribution = [
            [
                Counter(),
                Counter({((C, C), D): 3, ((C, D), D): 3, ((D, C), C): 6}),
                Counter(),
                Counter(),
            ],
            [
                Counter({((C, C), C): 3, ((D, C), C): 3, ((C, D), D): 6}),
                Counter(),
                Counter(),
                Counter(),
            ],
            [Counter(), Counter(), Counter(), Counter({((D, C), D): 12})],
            [Counter(), Counter(), Counter({((C, D), C): 12}), Counter()],
        ]

        cls.expected_normalised_state_to_action_distribution = [
            [
                Counter(),
                Counter({((C, C), D): 1.0, ((C, D), D): 1.0, ((D, C), C): 1.0}),
                Counter(),
                Counter(),
            ],
            [
                Counter({((C, C), C): 1.0, ((D, C), C): 1.0, ((C, D), D): 1.0}),
                Counter(),
                Counter(),
                Counter(),
            ],
            [Counter(), Counter(), Counter(), Counter({((D, C), D): 1.0})],
            [Counter(), Counter(), Counter({((C, D), C): 1.0}), Counter()],
        ]


class TestResultSetSpatialStructureThree(TestResultSetSpatialStructure):
    @classmethod
    def setUpClass(cls):

        path = pathlib.Path("test_outputs/test_results_spatial_three.csv")
        cls.filename = str(axl_filename(path))
        cls.players = [
            axl.Alternator(),
            axl.TitForTat(),
            axl.Defector(),
            axl.Cooperator(),
        ]
        cls.turns = 5
        cls.repetitions = 3
        cls.edges = [(0, 0), (1, 1), (2, 2), (3, 3)]

        cls.expected_match_lengths = [
            [[5, 0, 0, 0], [0, 5, 0, 0], [0, 0, 5, 0], [0, 0, 0, 5]]
            for _ in range(3)
        ]

        cls.expected_scores = [[0 for _ in range(3)] for _ in range(4)]

        cls.expected_wins = [[0 for _ in range(3)] for _ in range(4)]

        cls.expected_normalised_scores = [
            [0 for _ in range(3)] for i in range(4)
        ]

        cls.expected_ranking = [0, 1, 2, 3]

        cls.expected_ranked_names = [
            "Alternator",
            "Tit For Tat",
            "Defector",
            "Cooperator",
        ]

        cls.expected_null_results_matrix = [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ]

        cls.expected_payoffs = [
            [[11 / 5 for _ in range(3)], [], [], []],
            [[], [15 / 5 for _ in range(3)], [], []],
            [[], [], [5 / 5 for _ in range(3)], []],
            [[], [], [], [15 / 5 for _ in range(3)]],
        ]

        cls.expected_score_diffs = [
            [[0.0 for _ in range(3)] for _ in range(4)] for _ in range(4)
        ]

        cls.expected_payoff_diffs_means = [
            [0.0 for _ in range(4)] for _ in range(4)
        ]

        # Recalculating to deal with numeric imprecision
        cls.expected_payoff_matrix = [
            [mean([11 / 5 for _ in range(3)]), 0, 0, 0],
            [0, mean([15 / 5 for _ in range(3)]), 0, 0],
            [0, 0, mean([5 / 5 for _ in range(3)]), 0],
            [0, 0, 0, mean([15 / 5 for _ in range(3)])],
        ]

        cls.expected_payoff_stddevs = [
            [std([11 / 5 for _ in range(3)]), 0, 0, 0],
            [0, std([15 / 5 for _ in range(3)]), 0, 0],
            [0, 0, std([5 / 5 for _ in range(3)]), 0],
            [0, 0, 0, std([15 / 5 for _ in range(3)])],
        ]

        cls.expected_cooperation = [
            [9.0, 0, 0, 0],
            [0, 15.0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 15.0],
        ]

        cls.expected_normalised_cooperation = [
            [mean([3 / 5 for _ in range(3)]), 0.0, 0.0, 0.0],
            [0.0, mean([5 / 5 for _ in range(3)]), 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, mean([5 / 5 for _ in range(3)])],
        ]

        cls.expected_initial_cooperation_count = [0, 0, 0, 0]
        cls.expected_initial_cooperation_rate = [0, 0, 0, 0]

        cls.expected_vengeful_cooperation = [
            [2 * element - 1 for element in row]
            for row in cls.expected_normalised_cooperation
        ]

        cls.expected_cooperating_rating = [0.0 for _ in range(4)]

        cls.expected_good_partner_matrix = [
            [0.0 for _ in range(4)] for _ in range(4)
        ]

        cls.expected_good_partner_rating = [0.0 for _ in range(4)]

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
            0.3985944056208427,
        ]

        cls.expected_state_distribution = [
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
        ]

        cls.expected_normalised_state_distribution = [
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
        ]

        cls.expected_state_to_action_distribution = [
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
        ]

        cls.expected_normalised_state_to_action_distribution = [
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
            [Counter(), Counter(), Counter(), Counter()],
        ]

    def test_equality(self):
        """Overwriting for this particular case"""
        pass

    def test_summarise(self):
        """Overwriting for this particular case"""
        rs = axl.ResultSet(
            self.filename, self.players, self.repetitions, progress_bar=False
        )
        sd = rs.summarise()

        for player in sd:
            self.assertEqual(player.CC_rate, 0)
            self.assertEqual(player.CD_rate, 0)
            self.assertEqual(player.DC_rate, 0)
            self.assertEqual(player.DD_rate, 0)


class TestSummary(unittest.TestCase):
    """Separate test to check that summary always builds without failures"""

    @given(
        tournament=tournaments(
            min_size=2, max_size=5, max_turns=5, max_repetitions=3
        )
    )
    @settings(max_examples=5, deadline=None)
    def test_summarise_without_failure(self, tournament):
        results = tournament.play(progress_bar=False)
        sd = results.summarise()
        self.assertIsInstance(sd, list)

        for player in sd:
            # round for numerical error
            total_rate = round(
                player.CC_rate
                + player.CD_rate
                + player.DC_rate
                + player.DD_rate,
                3,
            )
            self.assertTrue(total_rate in [0, 1])
            self.assertTrue(0 <= player.Initial_C_rate <= 1)


class TestCreateCounterDict(unittest.TestCase):
    """Separate test for a helper function"""

    def test_basic_use(self):
        key_map = {"Col 1": "Var 1", "Col 2": "Var 2"}
        df = pd.DataFrame(
            {"Col 1": [10, 20, 30], "Col 2": [1, 2, 0]},
            index=[[5, 6, 7], [1, 2, 3]],
        )
        self.assertEqual(
            create_counter_dict(df, 6, 2, key_map),
            Counter({"Var 1": 20, "Var 2": 2}),
        )
        self.assertEqual(
            create_counter_dict(df, 7, 3, key_map), Counter({"Var 1": 30})
        )
