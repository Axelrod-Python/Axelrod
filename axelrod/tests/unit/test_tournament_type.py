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

    def test_round_robin(self):
        matches = axelrod.tournament_type.round_robin(
            players=self.players,
            opponents=self.players,
            turns=test_turns,
            deterministic_cache={}
        )
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
