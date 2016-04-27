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
test_repetitions = 10
test_game = axelrod.Game()


class TestTournamentType(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    def test_init_with_clone(self):
        tt = axelrod.MatchGenerator(
            self.players, test_turns, test_game, test_repetitions, axelrod.DeterministicCache())
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

    def test_build_single_match(self):
        rr = axelrod.RoundRobinMatches(
            self.players, test_turns, test_game, test_repetitions, axelrod.DeterministicCache())
        match = rr.build_single_match((self.players[0], self.players[1]))
        self.assertIsInstance(match, axelrod.Match)
        self.assertEqual(len(match), rr.turns)


    @given(chunk_size=integers(min_value=1, max_value=test_repetitions),
           repetitions=integers(min_value=1, max_value=test_repetitions))
    @example(chunk_size=5, repetitions=test_repetitions)
    def test_build_match_chunks(self, chunk_size, repetitions):
        rr = axelrod.RoundRobinMatches(
            self.players, test_turns, test_game, repetitions,
            axelrod.DeterministicCache(), chunk_size)
        chunks = list(rr.build_match_chunks())
        match_definitions = [index_pair for chunk in chunks for index_pair, match in
                chunk]
        expected_match_definitions = [(i, j) for i in range(5) for j in range(i, 5)
                for r in range(repetitions)]

        self.assertEqual(sorted(match_definitions), sorted(expected_match_definitions))

        # Check chunk size
        for chunk in chunks[:-1]:
            self.assertEqual(len(chunk), chunk_size)
        self.assertLessEqual(len(chunks[-1]), chunk_size)


class TestProbEndRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    @given(chunk_size=integers(min_value=1, max_value=test_repetitions),
           repetitions=integers(min_value=1, max_value=test_repetitions),
           prob_end=floats(min_value=0, max_value=1), rm=random_module())
    @example(chunk_size=5, repetitions=test_repetitions, prob_end=.5,
            rm=random_module())
    def test_build_match_chunks(self, chunk_size, repetitions, prob_end, rm):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, repetitions,
            axelrod.DeterministicCache(), chunk_size)
        chunks = list(rr.build_match_chunks())
        match_definitions = [index_pair for chunk in chunks for index_pair, match in
                chunk]
        expected_match_definitions = [(i, j) for i in range(5) for j in range(i, 5)
                for r in range(repetitions)]

        self.assertEqual(sorted(match_definitions), sorted(expected_match_definitions))

        # Check chunk size
        for chunk in chunks[:-1]:
            self.assertEqual(len(chunk), chunk_size)
        self.assertLessEqual(len(chunks[-1]), chunk_size)

    @given(prob_end=floats(min_value=0.1, max_value=0.5), rm=random_module())
    def test_build_matches_different_length(self, prob_end, rm):
        """
        If prob end is not 0 or 1 then the matches should all have different
        length

        Theoretically, this test could fail as it's probabilistically possible
        to sample all games with same length.
        """
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions, axelrod.DeterministicCache())
        chunks = rr.build_match_chunks()
        match_lengths = [len(match) for chunk in chunks for index_pair, match in chunk]
        self.assertNotEqual(min(match_lengths), max(match_lengths))

    @given(prob_end=floats(min_value=0, max_value=1), rm=random_module())
    def test_sample_length(self, prob_end, rm):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions, axelrod.DeterministicCache())
        self.assertGreaterEqual(rr.sample_length(prob_end), 1)
        try:
            self.assertIsInstance(rr.sample_length(prob_end), int)
        except AssertionError:
            self.assertEqual(rr.sample_length(prob_end), float("inf"))

    @given(prob_end=floats(min_value=.1, max_value=1), rm=random_module())
    def test_build_single_match(self, prob_end, rm):
        rr = axelrod.ProbEndRoundRobinMatches(
            self.players, prob_end, test_game, test_repetitions, axelrod.DeterministicCache())
        match = rr.build_single_match((self.players[0], self.players[1]))

        self.assertIsInstance(match, axelrod.Match)
        self.assertGreaterEqual(len(match), 1)
        self.assertLessEqual(len(match), float("inf"))
