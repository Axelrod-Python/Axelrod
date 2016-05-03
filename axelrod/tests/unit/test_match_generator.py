import unittest
import axelrod

from hypothesis import given, example
from hypothesis.strategies import floats, random_module, integers

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
        match_params = rr.build_single_match_params(noise=.5)
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
        #match_definitions = [tuple(list(index_pair) + [repetitions]) for (index_pair, match_params, repetitions) in chunks]
        match_definitions = [tuple(list(index_pair) + [repetitions]) for (index_pair, match_params, repetitions) in chunks]
        expected_match_definitions = [(i, j, repetitions) for i in range(5) for j in range(i, 5)]

        self.assertEqual(sorted(match_definitions), sorted(expected_match_definitions))

class TestProbEndRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    @given(repetitions=integers(min_value=1, max_value=test_repetitions),
           prob_end=floats(min_value=0, max_value=1), rm=random_module())
    @example(repetitions=test_repetitions, prob_end=.5, rm=random_module())
    def test_build_match_chunks(self, repetitions, prob_end, rm):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, repetitions)
        chunks = list(rr.build_match_chunks())
        match_definitions = [tuple(list(index_pair) + [repetitions]) for (index_pair, match_params, repetitions) in chunks]
        expected_match_definitions = [(i, j, repetitions) for i in range(5) for j in range(i, 5)]

        self.assertEqual(sorted(match_definitions), sorted(expected_match_definitions))

    @given(prob_end=floats(min_value=0.1, max_value=0.5), rm=random_module())
    def test_build_matches_different_length(self, prob_end, rm):
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

    @given(prob_end=floats(min_value=0, max_value=1), rm=random_module())
    def test_sample_length(self, prob_end, rm):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions)
        self.assertGreaterEqual(rr.sample_length(prob_end), 1)
        try:
            self.assertIsInstance(rr.sample_length(prob_end), int)
        except AssertionError:
            self.assertEqual(rr.sample_length(prob_end), float("inf"))

    @given(prob_end=floats(min_value=.1, max_value=1), rm=random_module())
    def test_build_single_match_params(self, prob_end, rm):
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

        # Testing with noise
        match_params = rr.build_single_match_params(noise=.5)
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
