import unittest

import axelrod as axl

C, D = axl.Action.C, axl.Action.D


class TestSampleTournaments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = axl.Game()

    @classmethod
    def get_test_outcome(cls, outcome, turns=10):
        # Extract the name of players from the outcome tuples,
        # and initiate the players by getting the classes from axelrod.
        names = [out[0] for out in outcome]
        players = [getattr(axl, n)() for n in names]

        # Play the tournament and build the actual outcome tuples.
        tournament = axl.Tournament(
            players=players, game=cls.game, turns=turns, repetitions=1
        )
        results = tournament.play(progress_bar=False)
        scores = [score[0] for score in results.scores]
        outcome = zip(names, scores)

        # Return the outcome sorted by score
        return sorted(outcome, key=lambda k: k[1])

    def test_defector_v_cooperator(self):
        """Test: the defector viciously punishes the cooperator."""
        outcome = [("Cooperator", 0), ("Defector", 50)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_defector_v_titfortat(self):
        """Test: the defector does well against tit for tat."""
        outcome = [("TitForTat", 9), ("Defector", 14)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_cooperator_v_titfortat(self):
        """Test: the cooperator does very well WITH tit for tat."""
        outcome = [("Cooperator", 30), ("TitForTat", 30)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_cooperator_v_titfortat_v_defector(self):
        """Test: the defector dominates in this population."""
        outcome = [("Cooperator", 30), ("TitForTat", 39), ("Defector", 64)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_cooperator_v_titfortat_v_defector_v_grudger(self):
        """Test: tit for tat does better this time around."""
        outcome = [
            ("Cooperator", 60),
            ("TitForTat", 69),
            ("Grudger", 69),
            ("Defector", 78),
        ]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_cooperator_v_titfortat_v_defector_v_grudger_v_go_by_majority(self):
        """Test: Tit for tat is doing a lot better."""
        outcome = [
            ("Cooperator", 90),
            ("Defector", 92),
            ("Grudger", 99),
            ("GoByMajority", 99),
            ("TitForTat", 99),
        ]
        self.assertEqual(self.get_test_outcome(outcome), outcome)
