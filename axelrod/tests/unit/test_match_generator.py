import unittest

from hypothesis import example, given, settings
from hypothesis.strategies import integers

import axelrod as axl
from axelrod.match_generator import graph_is_connected

test_strategies = [
    axl.Cooperator,
    axl.TitForTat,
    axl.Defector,
    axl.Grudger,
    axl.GoByMajority,
]
test_turns = 100
test_repetitions = 20
test_game = axl.Game()


class TestMatchGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    def test_build_single_match_params(self):
        rr = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=test_repetitions,
        )
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, dict)
        self.assertEqual(match_params["turns"], test_turns)
        self.assertEqual(match_params["game"], test_game)
        self.assertEqual(match_params["noise"], 0)
        self.assertIsNone(match_params["prob_end"])

        # Check that can build a match
        players = [axl.Cooperator(), axl.Defector()]
        match_params["players"] = players
        match = axl.Match(**match_params)
        self.assertIsInstance(match, axl.Match)
        self.assertEqual(len(match), test_turns)

    def test_build_single_match_params_with_noise(self):
        rr = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=test_repetitions,
            noise=0.5,
        )
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, dict)
        self.assertEqual(match_params["turns"], test_turns)
        self.assertEqual(match_params["game"], test_game)
        self.assertEqual(match_params["noise"], 0.5)
        self.assertIsNone(match_params["prob_end"])

        # Check that can build a match
        players = [axl.Cooperator(), axl.Defector()]
        match_params["players"] = players
        match = axl.Match(**match_params)
        self.assertIsInstance(match, axl.Match)
        self.assertEqual(len(match), test_turns)

    def test_build_single_match_params_with_prob_end(self):
        rr = axl.MatchGenerator(
            players=self.players,
            game=test_game,
            repetitions=test_repetitions,
            prob_end=0.5,
        )
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, dict)
        self.assertIsNone(match_params["turns"])
        self.assertEqual(match_params["game"], test_game)
        self.assertEqual(match_params["noise"], 0)
        self.assertEqual(match_params["prob_end"], 0.5)

        # Check that can build a match
        players = [axl.Cooperator(), axl.Defector()]
        match_params["players"] = players
        match = axl.Match(**match_params)
        self.assertIsInstance(match, axl.Match)
        with self.assertRaises(TypeError):
            len(match)

    def test_build_single_match_params_with_prob_end_and_noise(self):
        rr = axl.MatchGenerator(
            players=self.players,
            game=test_game,
            repetitions=test_repetitions,
            noise=0.5,
            prob_end=0.5,
        )
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, dict)
        self.assertIsNone(match_params["turns"])
        self.assertEqual(match_params["game"], rr.game)
        self.assertEqual(match_params["prob_end"], 0.5)
        self.assertEqual(match_params["noise"], 0.5)

        # Check that can build a match
        players = [axl.Cooperator(), axl.Defector()]
        match_params["players"] = players
        match = axl.Match(**match_params)
        self.assertIsInstance(match, axl.Match)
        with self.assertRaises(TypeError):
            len(match)

    def test_build_single_match_params_with_prob_end_and_turns(self):
        rr = axl.MatchGenerator(
            players=self.players,
            game=test_game,
            repetitions=test_repetitions,
            turns=5,
            prob_end=0.5,
        )
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, dict)
        self.assertEqual(match_params["turns"], 5)
        self.assertEqual(match_params["game"], test_game)
        self.assertEqual(match_params["prob_end"], 0.5)
        self.assertEqual(match_params["noise"], 0)

        # Check that can build a match
        players = [axl.Cooperator(), axl.Defector()]
        match_params["players"] = players
        match = axl.Match(**match_params)
        self.assertIsInstance(match, axl.Match)
        self.assertIsInstance(len(match), int)
        self.assertGreater(len(match), 0)
        self.assertLessEqual(len(match), 10)

    def test_build_single_match_params_with_fixed_length_unknown(self):
        rr = axl.MatchGenerator(
            players=self.players,
            game=test_game,
            repetitions=test_repetitions,
            turns=5,
            match_attributes={"length": float("inf")},
        )
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, dict)
        self.assertEqual(match_params["turns"], 5)
        self.assertEqual(match_params["game"], test_game)
        self.assertEqual(match_params["prob_end"], None)
        self.assertEqual(match_params["noise"], 0)
        self.assertEqual(
            match_params["match_attributes"], {"length": float("inf")}
        )

        # Check that can build a match
        players = [axl.Cooperator(), axl.Defector()]
        match_params["players"] = players
        match = axl.Match(**match_params)
        self.assertIsInstance(match, axl.Match)
        self.assertEqual(len(match), 5)
        self.assertEqual(match.match_attributes, {"length": float("inf")})

    @given(repetitions=integers(min_value=1, max_value=test_repetitions))
    @settings(max_examples=5)
    @example(repetitions=test_repetitions)
    def test_build_match_chunks(self, repetitions):
        rr = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=repetitions,
        )
        chunks = list(rr.build_match_chunks())
        match_definitions = [
            tuple(list(index_pair) + [repetitions])
            for (index_pair, match_params, repetitions, _) in chunks
        ]
        expected_match_definitions = [
            (i, j, repetitions) for i in range(5) for j in range(i, 5)
        ]

        self.assertEqual(
            sorted(match_definitions), sorted(expected_match_definitions)
        )

    @given(
        repetitions=integers(min_value=1, max_value=test_repetitions),
        seed=integers(min_value=1, max_value=4294967295),
    )
    @settings(max_examples=5)
    def test_seeding_equality(self, repetitions, seed):
        rr1 = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=repetitions,
            seed=seed,
        )
        chunks1 = list(rr1.build_match_chunks())
        rr2 = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=repetitions,
            seed=seed,
        )
        chunks2 = list(rr2.build_match_chunks())
        self.assertEqual(chunks1, chunks2)

    def test_seeding_inequality(self, repetitions=10):
        rr1 = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=repetitions,
            seed=0,
        )
        chunks1 = list(rr1.build_match_chunks())
        rr2 = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=repetitions,
            seed=1,
        )
        chunks2 = list(rr2.build_match_chunks())
        self.assertNotEqual(chunks1, chunks2)

    @given(repetitions=integers(min_value=1, max_value=test_repetitions))
    @settings(max_examples=5)
    @example(repetitions=test_repetitions)
    def test_spatial_build_match_chunks(self, repetitions):
        cycle = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 1)]
        rr = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            edges=cycle,
            repetitions=repetitions,
        )
        chunks = list(rr.build_match_chunks())
        match_definitions = [
            tuple(list(index_pair) + [repetitions])
            for (index_pair, match_params, repetitions, _) in chunks
        ]
        expected_match_definitions = [(i, j, repetitions) for i, j in cycle]

        self.assertEqual(
            sorted(match_definitions), sorted(expected_match_definitions)
        )

    def test_len(self):
        turns = 5
        repetitions = 10
        rr = axl.MatchGenerator(
            players=self.players,
            turns=test_turns,
            game=test_game,
            repetitions=test_repetitions,
        )
        self.assertEqual(len(rr), len(list(rr.build_match_chunks())))

    def test_init_with_graph_edges_not_including_all_players(self):
        edges = [(0, 1), (1, 2)]
        with self.assertRaises(ValueError):
            axl.MatchGenerator(
                players=self.players,
                repetitions=3,
                game=test_game,
                turns=5,
                edges=edges,
                noise=0,
            )


class TestUtilityFunctions(unittest.TestCase):
    def test_connected_graph(self):
        edges = [(0, 0), (0, 1), (1, 1)]
        players = ["Cooperator", "Defector"]
        self.assertTrue(graph_is_connected(edges, players))

    def test_unconnected_graph(self):
        edges = [(0, 0), (0, 1), (1, 1)]
        players = ["Cooperator", "Defector", "Alternator"]
        self.assertFalse(graph_is_connected(edges, players))
