import unittest

from hypothesis import given, example
from hypothesis.strategies import floats, integers

import axelrod
from axelrod.match_generator import graph_is_connected


test_strategies = [
    axelrod.Cooperator,
    axelrod.TitForTat,
    axelrod.Defector,
    axelrod.Grudger,
    axelrod.GoByMajority
]
test_turns = 100
test_repetitions = 20
test_game = axelrod.Game()


class TestTournamentType(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    def test_init_with_clone(self):
        tt = axelrod.MatchGenerator(
            self.players, test_turns, test_game, test_repetitions)
        self.assertEqual(tt.players, self.players)
        self.assertEqual(tt.turns, test_turns)
        player = tt.players[0]
        opponent = tt.opponents[0]
        self.assertEqual(player.name, opponent.name)
        self.assertNotEqual(player, opponent)
        # Check that the two player instances are wholly independent
        opponent.name = 'Test'
        self.assertNotEqual(player.name, opponent.name)

    def test_len(self):
        tt = axelrod.MatchGenerator(
            self.players, test_turns, test_game, test_repetitions)
        with self.assertRaises(NotImplementedError):
            len(tt)

    def test_build_match_params(self):
        tt = axelrod.MatchGenerator(
            self.players, test_turns, test_game, test_repetitions)
        with self.assertRaises(NotImplementedError):
            tt.build_match_chunks()

    def test_single_match_params(self):
        tt = axelrod.MatchGenerator(
            self.players, test_turns, test_game, test_repetitions)
        with self.assertRaises(NotImplementedError):
            tt.build_single_match_params()


class TestRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    def test_build_single_match_params(self):
        rr = axelrod.RoundRobinMatches(
            self.players, test_turns, test_game, test_repetitions)
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, tuple)
        self.assertEqual(match_params[0], rr.turns)
        self.assertEqual(match_params[1], rr.game)
        self.assertEqual(match_params[2], None)
        self.assertEqual(match_params[3], 0)

        # Check that can build a match
        players = [axelrod.Cooperator(), axelrod.Defector()]
        match_params = [players] + list(match_params)
        match = axelrod.Match(*match_params)
        self.assertIsInstance(match, axelrod.Match)
        self.assertEqual(len(match), test_turns)

        # Testing with noise
        rr = axelrod.RoundRobinMatches(
            self.players, test_turns, test_game, test_repetitions, noise=0.5)
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, tuple)
        self.assertEqual(match_params[0], rr.turns)
        self.assertEqual(match_params[1], rr.game)
        self.assertEqual(match_params[2], None)
        self.assertEqual(match_params[3], .5)

        # Check that can build a match
        players = [axelrod.Cooperator(), axelrod.Defector()]
        match_params = [players] + list(match_params)
        match = axelrod.Match(*match_params)
        self.assertIsInstance(match, axelrod.Match)
        self.assertEqual(len(match), test_turns)

    @given(repetitions=integers(min_value=1, max_value=test_repetitions))
    @example(repetitions=test_repetitions)
    def test_build_match_chunks(self, repetitions):
        rr = axelrod.RoundRobinMatches(self.players, test_turns, test_game, repetitions)
        chunks = list(rr.build_match_chunks())
        match_definitions = [tuple(list(index_pair) + [repetitions]) for (index_pair, match_params, repetitions) in chunks]
        expected_match_definitions = [(i, j, repetitions) for i in range(5) for j in range(i, 5)]

        self.assertEqual(sorted(match_definitions), sorted(expected_match_definitions))

    def test_len(self):
        turns = 5
        repetitions = 10
        rr = axelrod.RoundRobinMatches(self.players, turns=turns, game=None,
                                       repetitions=repetitions)
        self.assertEqual(len(rr), len(list(rr.build_match_chunks())))
        self.assertEqual(rr.estimated_size(), len(rr) * turns * repetitions)


class TestProbEndRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    @given(repetitions=integers(min_value=1, max_value=test_repetitions),
           prob_end=floats(min_value=0, max_value=1))
    @example(repetitions=test_repetitions, prob_end=.5)
    def test_build_match_chunks(self, repetitions, prob_end):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, repetitions)
        chunks = list(rr.build_match_chunks())
        match_definitions = [tuple(list(index_pair) + [repetitions]) for (index_pair, match_params, repetitions) in chunks]
        expected_match_definitions = [(i, j, repetitions) for i in range(5) for j in range(i, 5)]

        self.assertEqual(sorted(match_definitions), sorted(expected_match_definitions))

    @given(prob_end=floats(min_value=0.1, max_value=0.5))
    def test_build_matches_different_length(self, prob_end):
        """
        If prob end is not 0 or 1 then the matches should all have different
        length

        Theoretically, this test could fail as it's probabilistically possible
        to sample all games with same length.
        """
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions)
        chunks = rr.build_match_chunks()
        match_lengths = [match_params[0] for (index_pair, match_params, repetitions) in chunks]
        self.assertNotEqual(min(match_lengths), max(match_lengths))

    @given(prob_end=floats(min_value=0, max_value=1))
    def test_sample_length(self, prob_end):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions,
        )
        self.assertGreaterEqual(rr.sample_length(), 1)
        try:
            self.assertIsInstance(rr.sample_length(), int)
        except AssertionError:
            self.assertEqual(rr.sample_length(), float("inf"))

    @given(prob_end=floats(min_value=.1, max_value=1))
    def test_build_single_match_params(self, prob_end):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions)
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, tuple)
        self.assertIsInstance(match_params[0], int)
        self.assertLess(match_params[0], float('inf'))
        self.assertGreater(match_params[0], 0)
        self.assertEqual(match_params[1], rr.game)
        self.assertEqual(match_params[2], None)
        self.assertEqual(match_params[3], 0)

        # Check that can build a match
        players = [axelrod.Cooperator(), axelrod.Defector()]
        match_params = [players] + list(match_params)
        match = axelrod.Match(*match_params)
        self.assertIsInstance(match, axelrod.Match)
        self.assertLess(len(match), float('inf'))
        self.assertGreater(len(match), 0)
        self.assertEqual(match.players[0].match_attributes['length'], float('inf'))

        # Testing with noise
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions, noise=0.5)
        match_params = rr.build_single_match_params()
        self.assertIsInstance(match_params, tuple)
        self.assertLess(match_params[0], float('inf'))
        self.assertGreater(match_params[0], 0)
        self.assertEqual(match_params[1], rr.game)
        self.assertEqual(match_params[2], None)
        self.assertEqual(match_params[3], .5)

        # Check that can build a match
        players = [axelrod.Cooperator(), axelrod.Defector()]
        match_params = [players] + list(match_params)
        match = axelrod.Match(*match_params)
        self.assertIsInstance(match, axelrod.Match)
        self.assertLess(len(match), float('inf'))
        self.assertGreater(len(match), 0)

    @given(prob_end=floats(min_value=.1, max_value=1))
    def test_len(self, prob_end):
        repetitions = 10
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, game=None, repetitions=repetitions)
        self.assertEqual(len(rr), len(list(rr.build_match_chunks())))
        self.assertAlmostEqual(rr.estimated_size(), len(rr) * 1. / prob_end * repetitions)


class TestSpatialMatches(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    @given(repetitions=integers(min_value=1, max_value=test_repetitions),
           turns=integers(min_value=1, max_value=test_turns),
           noise=floats(min_value=0, max_value=1))
    @example(repetitions=test_repetitions, turns=test_turns, noise=0)
    def test_build_match_chunks(self, repetitions, turns, noise):
        edges = [(0, 1), (1, 2), (3, 4)]
        sp = axelrod.SpatialMatches(
            self.players, turns, test_game, repetitions, edges, noise)
        chunks = list(sp.build_match_chunks())

        match_definitions = set()

        cache = None
        expected_params = (turns, test_game, cache, noise)
        for index_pair, match_params, repetitions in chunks:
            match_definitions.add(tuple(list(index_pair) + [repetitions]))
            self.assertEqual(match_params, expected_params)

        expected_match_definitions = set((edge[0], edge[1], repetitions)
                                         for edge in edges)

        self.assertEqual(match_definitions, expected_match_definitions)

    def test_len(self):
        edges = [(0, 1), (1, 2), (3, 4)]
        sp = axelrod.SpatialMatches(
            self.players, test_turns, test_game, test_repetitions, edges)
        self.assertEqual(len(sp), len(list(sp.build_match_chunks())))
        self.assertEqual(len(sp), len(edges))


class TestProbEndSpatialMatches(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    @given(repetitions=integers(min_value=1, max_value=test_repetitions),
           prob_end=floats(min_value=.2, max_value=.7),
           noise=floats(min_value=0, max_value=1))
    @example(repetitions=test_repetitions, prob_end=.5, noise=0)
    def test_build_match_chunks(self, repetitions, prob_end, noise):
        edges = [(0, 1), (1, 2), (3, 4)]
        pesp = axelrod.ProbEndSpatialMatches(
            self.players, prob_end, test_game, repetitions, noise, edges)
        chunks = list(pesp.build_match_chunks())

        match_definitions = set()

        cache = None
        attributes = {'game': test_game, 'length': float('inf'), 'noise': noise}
        expected_params_without_turns = (test_game, cache, noise, attributes)

        for index_pair, match_params, repetitions in chunks:
            match_definitions.add(tuple(list(index_pair) + [repetitions]))
            self.assertEqual(match_params[1:], expected_params_without_turns)

        expected_match_definitions = set((edge[0], edge[1], repetitions)
                                         for edge in edges)

        self.assertEqual(match_definitions, expected_match_definitions)

    def test_raise_error_if_not_connected(self):
        edges = [(0, 0), (0, 1), (1, 1)]
        players = ["Cooperator", "Defector", "Alternator"]
        noise = 0
        self.assertRaises(ValueError, axelrod.ProbEndSpatialMatches,
                          players, test_turns, test_game, test_repetitions,
                          noise, edges)

    def test_len(self):
        edges = [(0, 1), (1, 2), (3, 4)]
        noise = 0
        pesp = axelrod.ProbEndSpatialMatches(
            self.players, test_turns, test_game, test_repetitions, noise, edges)
        self.assertEqual(len(pesp), len(list(pesp.build_match_chunks())))
        self.assertEqual(len(pesp), len(edges))

    @given(prob_end=floats(min_value=0, max_value=1))
    def test_sample_length(self, prob_end):
        edges = [(0, 1), (1, 2), (3, 4)]
        noise = 0
        pesp = axelrod.ProbEndSpatialMatches(
            self.players, prob_end, test_game, test_repetitions, noise, edges)
        self.assertGreaterEqual(pesp.sample_length(), 1)
        try:
            self.assertIsInstance(pesp.sample_length(), int)
        except AssertionError:
            self.assertEqual(pesp.sample_length(), float("inf"))

    @given(prob_end=floats(min_value=0.005, max_value=0.01))
    def test_build_matches_different_length(self, prob_end):
        """
        If prob end is not 0 or 1 then the matches should all have different
        length

        Theoretically, this test could fail as it's probabilistically possible
        to sample all games with same length.
        """
        edges = [(0, 1), (1, 2), (3, 4)]
        noise = 0
        pesp = axelrod.ProbEndSpatialMatches(
            self.players, prob_end, test_game, test_repetitions, noise, edges)
        chunks = pesp.build_match_chunks()
        match_lengths = [match_params[0]
                         for (index_pair, match_params, repetitions) in chunks]
        self.assertNotEqual(min(match_lengths), max(match_lengths))

    @given(noise=floats(min_value=0, max_value=1),
           prob_end=floats(min_value=0, max_value=1))
    def test_noise(self, noise, prob_end):
        edges = [(0, 1), (1, 2), (3, 4)]
        pesp = axelrod.ProbEndSpatialMatches(
            self.players, prob_end, test_game, test_repetitions, noise, edges)
        self.assertEqual(pesp.noise, noise)
        chunks = pesp.build_match_chunks()
        noise_values = [match_params[3]
                        for (index_pair, match_params, repetitions) in chunks]
        for value in noise_values:
            self.assertEqual(noise, value)


class TestUtilityFunctions(unittest.TestCase):
    def test_connected_graph(self):
        edges = [(0, 0), (0, 1), (1, 1)]
        players = ["Cooperator", "Defector"]
        self.assertTrue(graph_is_connected(edges, players))

    def test_unconnected_graph(self):
        edges = [(0, 0), (0, 1), (1, 1)]
        players = ["Cooperator", "Defector", "Alternator"]
        self.assertFalse(graph_is_connected(edges, players))
