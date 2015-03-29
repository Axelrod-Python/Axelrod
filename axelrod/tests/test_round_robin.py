import unittest
import axelrod


class TestRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    @classmethod
    def payoffs2scores(cls, payoffs):
        return [sum([pp for ipp,pp in enumerate(p) if ipp != ip]) for ip,p in enumerate(payoffs)]

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

    def test_init(self):
        p1, p2 = axelrod.Player(), axelrod.Player()
        rr = axelrod.RoundRobin(players=[p1, p2], game=self.game, turns=20)
        self.assertEquals(rr.players, [p1, p2])
        self.assertEquals(rr.nplayers, 2)
        self.assertEquals(rr.game.score(('C', 'C')), (2, 2))

    def test_deterministic_cache(self):
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(players=[p1, p2, p3], game=self.game, turns=20)
        self.assertEquals(rr.deterministic_cache, {})
        rr.play()
        self.assertEqual(rr.deterministic_cache[(axelrod.Defector, axelrod.Defector)], (80, 80))
        self.assertEqual(rr.deterministic_cache[(axelrod.Cooperator, axelrod.Cooperator)], (40, 40))
        self.assertEqual(rr.deterministic_cache[(axelrod.Cooperator, axelrod.Defector)], (100, 0))
        self.assertFalse((axelrod.Random, axelrod.Random) in rr.deterministic_cache)

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
