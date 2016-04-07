# -*- coding: utf-8 -*-
import unittest
import axelrod.interaction_utils as iu
from axelrod import Actions

C, D = Actions.C, Actions.D


class TestMatch(unittest.TestCase):
    interactions = [
            [(C, D), (D, C)],
            [(D, C), (D, C)],
            [(C, C), (C, D)],
            [],
            ]


    scores = [
            [(0, 5), (5, 0)],
            [(5, 0), (5, 0)],
            [(3, 3), (0, 5)],
            [],
            ]


    final_scores = [
            (5, 5),
            (10, 0),
            (3, 8),
            None,
            ]


    final_score_per_turn = [
            (2.5, 2.5),
            (5, 0),
            (1.5, 4),
            None,
            ]

    winners = [False, 0, 1, None]
    cooperations = [(1, 1), (0, 2), (2, 1), None]
    normalised_cooperations = [(.5, .5), (0, 1), (1, .5), None]

    sparklines = [
            u'█ \n █',
            u'  \n██',
            u'██\n█ ',
            None
            ]


    def test_compute_scores(self):
        for inter, score in zip(self.interactions, self.scores):
            self.assertEqual(score, iu.compute_scores(inter))

    def test_compute_final_score(self):
        for inter, final_score in zip(self.interactions, self.final_scores):
            self.assertEqual(final_score, iu.compute_final_score(inter))

    def test_compute_final_score_per_turn(self):
        for inter, final_score_per_round in zip(self.interactions,
                                                self.final_score_per_turn):
            self.assertEqual(final_score_per_round,
                             iu.compute_final_score_per_turn(inter))

    def test_compute_winner_index(self):
        for inter, winner in zip(self.interactions, self.winners):
            self.assertEqual(winner, iu.compute_winner_index(inter))

    def test_compute_cooperations(self):
        for inter, coop in zip(self.interactions, self.cooperations):
            self.assertEqual(coop, iu.compute_cooperations(inter))

    def test_compute_normalised_cooperations(self):
        for inter, coop in zip(self.interactions, self.normalised_cooperations):
            self.assertEqual(coop, iu.compute_normalised_cooperation(inter))

    def test_compute_sparklines(self):
        for inter, spark in zip(self.interactions, self.sparklines):
            self.assertEqual(spark, iu.compute_sparklines(inter))

    def test_string_to_interactions(self):
        string = 'CDCDDD'
        interactions = [('C', 'D'), ('C', 'D'), ('D', 'D')]
        self.assertEqual(iu.string_to_interactions(string), interactions)
