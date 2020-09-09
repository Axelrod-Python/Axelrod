import tempfile
import unittest
from collections import Counter

import axelrod as axl

C, D = axl.Action.C, axl.Action.D


class TestMatch(unittest.TestCase):
    interactions = [[(C, D), (D, C)], [(D, C), (D, C)], [(C, C), (C, D)], []]
    scores = [[(0, 5), (5, 0)], [(5, 0), (5, 0)], [(3, 3), (0, 5)], []]
    final_scores = [(5, 5), (10, 0), (3, 8), None]
    final_score_per_turn = [(2.5, 2.5), (5, 0), (1.5, 4), None]
    winners = [False, 0, 1, None]
    cooperations = [(1, 1), (0, 2), (2, 1), None]
    normalised_cooperations = [(0.5, 0.5), (0, 1), (1, 0.5), None]
    state_distribution = [
        Counter({(C, D): 1, (D, C): 1}),
        Counter({(D, C): 2}),
        Counter({(C, C): 1, (C, D): 1}),
        None,
    ]
    state_to_action_distribution = [
        [Counter({((C, D), D): 1}), Counter({((C, D), C): 1})],
        [Counter({((D, C), D): 1}), Counter({((D, C), C): 1})],
        [Counter({((C, C), C): 1}), Counter({((C, C), D): 1})],
        None,
    ]

    normalised_state_distribution = [
        Counter({(C, D): 0.5, (D, C): 0.5}),
        Counter({(D, C): 1.0}),
        Counter({(C, C): 0.5, (C, D): 0.5}),
        None,
    ]
    normalised_state_to_action_distribution = [
        [Counter({((C, D), D): 1}), Counter({((C, D), C): 1})],
        [Counter({((D, C), D): 1}), Counter({((D, C), C): 1})],
        [Counter({((C, C), C): 1}), Counter({((C, C), D): 1})],
        None,
    ]

    sparklines = ["█ \n █", "  \n██", "██\n█ ", None]

    def test_compute_scores(self):
        for inter, score in zip(self.interactions, self.scores):
            self.assertEqual(score, axl.interaction_utils.compute_scores(inter))

    def test_compute_final_score(self):
        for inter, final_score in zip(self.interactions, self.final_scores):
            self.assertEqual(
                final_score, axl.interaction_utils.compute_final_score(inter)
            )

    def test_compute_final_score_per_turn(self):
        for inter, final_score_per_round in zip(
            self.interactions, self.final_score_per_turn
        ):
            self.assertEqual(
                final_score_per_round,
                axl.interaction_utils.compute_final_score_per_turn(inter),
            )

    def test_compute_winner_index(self):
        for inter, winner in zip(self.interactions, self.winners):
            self.assertEqual(
                winner, axl.interaction_utils.compute_winner_index(inter)
            )

    def test_compute_cooperations(self):
        for inter, coop in zip(self.interactions, self.cooperations):
            self.assertEqual(
                coop, axl.interaction_utils.compute_cooperations(inter)
            )

    def test_compute_normalised_cooperations(self):
        for inter, coop in zip(self.interactions, self.normalised_cooperations):
            self.assertEqual(
                coop,
                axl.interaction_utils.compute_normalised_cooperation(inter),
            )

    def test_compute_state_distribution(self):
        for inter, dist in zip(self.interactions, self.state_distribution):
            self.assertEqual(
                dist, axl.interaction_utils.compute_state_distribution(inter)
            )

    def test_compute_normalised_state_distribution(self):
        for inter, dist in zip(
            self.interactions, self.normalised_state_distribution
        ):
            self.assertEqual(
                dist,
                axl.interaction_utils.compute_normalised_state_distribution(
                    inter
                ),
            )

    def test_compute_state_to_action_distribution(self):
        for inter, dist in zip(
            self.interactions, self.state_to_action_distribution
        ):
            self.assertEqual(
                dist,
                axl.interaction_utils.compute_state_to_action_distribution(
                    inter
                ),
            )
        inter = [(C, D), (D, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        expected_dist = [
            Counter(
                {
                    ((C, C), C): 1,
                    ((D, C), C): 1,
                    ((C, D), D): 2,
                    ((D, C), D): 1,
                    ((D, D), C): 1,
                }
            ),
            Counter(
                {((C, C), D): 1, ((C, D), C): 2, ((D, C), D): 2, ((D, D), C): 1}
            ),
        ]

        self.assertEqual(
            expected_dist,
            axl.interaction_utils.compute_state_to_action_distribution(inter),
        )

    def test_compute_normalised_state_to_action_distribution(self):
        for inter, dist in zip(
            self.interactions, self.normalised_state_to_action_distribution
        ):
            self.assertEqual(
                dist,
                axl.interaction_utils.compute_normalised_state_to_action_distribution(
                    inter
                ),
            )
        inter = [(C, D), (D, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        expected_dist = [
            Counter(
                {
                    ((C, C), C): 1,
                    ((D, C), C): 1 / 2,
                    ((C, D), D): 1,
                    ((D, C), D): 1 / 2,
                    ((D, D), C): 1,
                }
            ),
            Counter(
                {((C, C), D): 1, ((C, D), C): 1, ((D, C), D): 1, ((D, D), C): 1}
            ),
        ]
        self.assertEqual(
            expected_dist,
            axl.interaction_utils.compute_normalised_state_to_action_distribution(
                inter
            ),
        )

    def test_compute_sparklines(self):
        for inter, spark in zip(self.interactions, self.sparklines):
            self.assertEqual(
                spark, axl.interaction_utils.compute_sparklines(inter)
            )

    def test_read_interactions_from_file(self):
        tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        players = [axl.Cooperator(), axl.Defector()]
        tournament = axl.Tournament(players=players, turns=2, repetitions=3)
        tournament.play(filename=tmp_file.name)
        tmp_file.close()
        expected_interactions = {
            (0, 0): [[(C, C), (C, C)] for _ in range(3)],
            (0, 1): [[(C, D), (C, D)] for _ in range(3)],
            (1, 1): [[(D, D), (D, D)] for _ in range(3)],
        }
        interactions = axl.interaction_utils.read_interactions_from_file(
            tmp_file.name, progress_bar=False
        )
        self.assertEqual(expected_interactions, interactions)

    def test_string_to_interactions(self):
        string = "CDCDDD"
        interactions = [(C, D), (C, D), (D, D)]
        self.assertEqual(
            axl.interaction_utils.string_to_interactions(string), interactions
        )
