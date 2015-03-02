"""Tests for the main module."""
import unittest
import axelrod


class TestInitialisation(unittest.TestCase):

    def test_initialisation(self):
        """Test that can initiate a tournament."""
        P1 = axelrod.Defector()
        P2 = axelrod.Defector()
        P3 = axelrod.Defector()
        tournament = axelrod.Tournament([P1, P2, P3])
        self.assertEqual([str(s) for s in tournament.players], ['Defector', 'Defector', 'Defector'])
        self.assertEqual(tournament.nplayers, 3)
        self.assertEqual(tournament.plist, [0, 1, 2])
        self.assertEqual(tournament.game.score(('C', 'C')), (2, 2))
        self.assertEqual(tournament.turns, 200)
        self.assertEqual(tournament.replist, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


class TestRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    @classmethod
    def payoffs2scores(cls, payoffs):
        return [sum(p) for p in payoffs]

    @classmethod
    def get_test_outcome(cls, outcome, turns=10):

        # Extract the name of players from the outcome tupples,
        # and initiate the players by getting the classes from axelrod.
        names = [out[0] for out in outcome]
        players = [getattr(axelrod, n)() for n in names]

        # Do the actual game and build the expected outcome tuples.
        round_robin = axelrod.RoundRobin(players=players, game=cls.game, turns=turns)
        payoffs = round_robin.play()
        scores = cls.payoffs2scores(payoffs)
        outcome = zip(names, scores)

        # The outcome is expected to be sort by score.
        return sorted(outcome, key = lambda k: k[1])

    def test_calculate_score_for_mix(self):
        """Test that scores are calculated correctly."""
        P1 = axelrod.Defector()
        P1.history = ['C', 'C', 'D']
        P2 = axelrod.Defector()
        P2.history = ['C', 'D', 'D']
        round_robin = axelrod.RoundRobin(players=[P1, P2], game=self.game, turns=200)
        self.assertEqual(round_robin.calculate_scores(P1, P2), (11, 6))

    def test_calculate_score_for_all_cooperate(self):
        """Test that scores are calculated correctly."""
        P1 = axelrod.Player()
        P1.history = ['C', 'C', 'C']
        P2 = axelrod.Player()
        P2.history = ['C', 'C', 'C']
        round_robin = axelrod.RoundRobin(players=[P1, P2], game=self.game, turns=200)
        self.assertEqual(round_robin.calculate_scores(P1, P2), (6, 6))

    def test_calculate_score_for_all_defect(self):
        """Test that scores are calculated correctly."""
        P1 = axelrod.Player()
        P1.history = ['D', 'D', 'D']
        P2 = axelrod.Player()
        P2.history = ['D', 'D', 'D']
        round_robin = axelrod.RoundRobin(players=[P1, P2], game=self.game, turns=200)
        self.assertEqual(round_robin.calculate_scores(P1, P2), (12, 12))

    def test_round_robin_defector_v_cooperator(self):
        """Test round robin: the defector viciously punishes the cooperator."""
        outcome = [('Defector', 0), ('Cooperator', 50)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_defector_v_titfortat(self):
        """Test round robin: the defector does well against tit for tat."""
        outcome = [('Defector', 36), ('TitForTat', 41)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat(self):
        """Test round robin: the cooperator does very well WITH tit for tat."""
        outcome = [('Cooperator', 20), ('TitForTat', 20)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat_v_defector(self):
        """Test round robin: the defector seems to dominate in this small population."""
        outcome = [('Defector', 36), ('TitForTat', 61), ('Cooperator', 70)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat_v_defector_v_grudger(self):
        """Test round robin: tit for tat does a lot better this time around."""
        outcome = [('Defector', 72), ('TitForTat', 81), ('Grudger', 81), ('Cooperator', 90)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat_v_defector_v_grudger_v_go_by_majority(self):
        """Test round robin: Tit for tat now wins."""
        outcome = [('TitForTat', 101), ('Grudger', 101), ('GoByMajority', 101), ('Defector', 108), ('Cooperator', 110)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)


class TestTournament(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    def test_full_tournament(self):
        """A test to check that tournament runs with all non cheating strategies."""
        strategies = [strategy() for strategy in axelrod.strategies]
        tournament = axelrod.Tournament(players=strategies, game=self.game, turns=500, repetitions=2)
        output_of_tournament = tournament.play()
        self.assertEqual(type(output_of_tournament), list)
        self.assertEqual(len(output_of_tournament), len(strategies))

    def test_tournament(self):
        """Test tournament."""

        outcome = [
            ('Tit For Tat', [2001, 2001, 2001, 2001, 2001]),
            ('Cooperator', [2200, 2200, 2200, 2200, 2200]),
            ('Defector', [2388, 2388, 2388, 2388, 2388]),
            ('Grudger', [2001, 2001, 2001, 2001, 2001]),
            ('Go By Majority', [2001, 2001, 2001, 2001, 2001]),
        ]
        outcome.sort()

        P1 = axelrod.Cooperator()
        P2 = axelrod.TitForTat()
        P3 = axelrod.Defector()
        P4 = axelrod.Grudger()
        P5 = axelrod.GoByMajority()
        tournament = axelrod.Tournament(players=[P1, P2, P3, P4, P5], game=self.game, turns=200, repetitions=5)
        names = [str(p) for p in tournament.players]
        results = tournament.play()
        scores = [[sum([r[i] for r in res]) for i in range(5)] for res in results]
        self.assertEqual(sorted(zip(names, scores)), outcome)


class TestPlayer(unittest.TestCase):

    def test_initialisation(self):
        """Test that can initiate a player."""
        P1 = axelrod.Player()
        self.assertEqual(P1.history, [])

    def test_play(self):
        """Test that play method looks for attribute strategy (which does not exist)."""
        P1, P2 = axelrod.Player(), axelrod.Player()
        self.assertEquals(P1.play(P2), None)
        self.assertEquals(P2.play(P1), None)


class TestGame(unittest.TestCase):

    def test_score(self):
        g = axelrod.Game()
        self.assertEquals(g.score(('C', 'C')), (2, 2))
        self.assertEquals(g.score(('D', 'D')), (4, 4))
        self.assertEquals(g.score(('C', 'D')), (5, 0))
        self.assertEquals(g.score(('D', 'C')), (0, 5))


if __name__ == '__main__':
    unittest.main()
