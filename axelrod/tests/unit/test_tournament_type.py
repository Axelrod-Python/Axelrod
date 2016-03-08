import unittest
import axelrod

test_strategies = [
    axelrod.Cooperator,
    axelrod.TitForTat,
    axelrod.Defector,
    axelrod.Grudger,
    axelrod.GoByMajority
]
test_turns = 100


class TestTournamentType(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.players = [s() for s in test_strategies]

    def test_init_with_clone(self):
        tt = axelrod.TournamentType(self.players, test_turns, {})
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

    def test_build_matches(self):
        rr = axelrod.RoundRobin(self.players, test_turns, {})
        matches = rr.build_matches()
        match_definitions = [
            (match) for match in matches]
        expected_match_definitions = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 3),
            (3, 4),
            (4, 4)
        ]
        self.assertEqual(sorted(match_definitions), expected_match_definitions)
