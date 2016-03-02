import unittest
import random
import axelrod

C, D = axelrod.Actions.C, axelrod.Actions.D

class TestRoundRobin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.game = axelrod.Game()

    @classmethod
    def payoffs2scores(cls, payoffs):
        return [sum([pp for ipp, pp in enumerate(p) if ipp != ip])
                for ip, p in enumerate(payoffs)]

    @classmethod
    def get_test_outcome(cls, outcome, turns=10):

        # Extract the name of players from the outcome tupples,
        # and initiate the players by getting the classes from axelrod.
        names = [out[0] for out in outcome]
        players = [getattr(axelrod, n)() for n in names]

        # Do the actual game and build the expected outcome tuples.
        round_robin = axelrod.RoundRobin(
            players=players, game=cls.game, turns=turns)
        payoffs = round_robin.play()['payoff']
        scores = cls.payoffs2scores(payoffs)
        outcome = zip(names, scores)

        # The outcome is expected to be sort by score.
        return sorted(outcome, key=lambda k: k[1])

    def test_deterministic_cache(self):
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(players=[p1, p2, p3], game=self.game, turns=20)
        self.assertEqual(rr.deterministic_cache, {})
        rr.play()
        self.assertEqual(rr.deterministic_cache[
            (axelrod.Defector, axelrod.Defector)]['scores'], (20, 20))
        self.assertEqual(rr.deterministic_cache[
            (axelrod.Defector, axelrod.Defector)]['cooperation_rates'], (0, 0))
        self.assertEqual(rr.deterministic_cache[
            (axelrod.Cooperator, axelrod.Cooperator)]['scores'], (60, 60))
        self.assertEqual(rr.deterministic_cache[
            (axelrod.Cooperator, axelrod.Cooperator)]['cooperation_rates'], (20, 20))
        self.assertEqual(rr.deterministic_cache[
            (axelrod.Cooperator, axelrod.Defector)]['scores'], (0, 100))
        self.assertEqual(rr.deterministic_cache[
            (axelrod.Cooperator, axelrod.Defector)]['cooperation_rates'], (20, 0))
        self.assertFalse(
            (axelrod.Random, axelrod.Random) in rr.deterministic_cache)

    def test_noisy_cache(self):
        p1, p2, p3 = axelrod.Cooperator(), axelrod.Defector(), axelrod.Random()
        rr = axelrod.RoundRobin(
            players=[p1, p2, p3], game=self.game, turns=20, noise=0.2)
        rr.play()
        self.assertEqual(rr.deterministic_cache, {})

    def test_calculate_score_for_mix(self):
        """Test that scores are calculated correctly."""
        P1 = axelrod.Defector()
        P1.history = [C, C, D]
        P2 = axelrod.Defector()
        P2.history = [C, D, D]
        round_robin = axelrod.RoundRobin(
            players=[P1, P2], game=self.game, turns=200)
        self.assertEqual(round_robin._calculate_scores(P1, P2), (4, 9))

    def test_calculate_score_for_all_cooperate(self):
        """Test that scores are calculated correctly."""
        P1 = axelrod.Player()
        P1.history = [C, C, C]
        P2 = axelrod.Player()
        P2.history = [C, C, C]
        round_robin = axelrod.RoundRobin(
            players=[P1, P2], game=self.game, turns=200)
        self.assertEqual(round_robin._calculate_scores(P1, P2), (9, 9))

    def test_calculate_score_for_all_defect(self):
        """Test that scores are calculated correctly."""
        P1 = axelrod.Player()
        P1.history = [D, D, D]
        P2 = axelrod.Player()
        P2.history = [D, D, D]
        round_robin = axelrod.RoundRobin(
            players=[P1, P2], game=self.game, turns=200)
        self.assertEqual(round_robin._calculate_scores(P1, P2), (3, 3))

    def test_round_robin_defector_v_cooperator(self):
        """Test round robin: the defector viciously punishes the cooperator."""
        outcome = [('Cooperator', 0), ('Defector', 50)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_defector_v_titfortat(self):
        """Test round robin: the defector does well against tit for tat."""
        outcome = [('TitForTat', 9), ('Defector', 14)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat(self):
        """Test round robin: the cooperator does very well WITH tit for tat."""
        outcome = [('Cooperator', 30), ('TitForTat', 30)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat_v_defector(self):
        """Test round robin: the defector dominates in this population."""
        outcome = [('Cooperator', 30), ('TitForTat', 39), ('Defector', 64)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat_v_defector_v_grudger(self):
        """Test round robin: tit for tat does better this time around."""
        outcome = [
            ('Cooperator', 60),
            ('TitForTat', 69),
            ('Grudger', 69),
            ('Defector', 78)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)

    def test_round_robin_cooperator_v_titfortat_v_defector_v_grudger_v_go_by_majority(self):
        """Test round robin: Tit for tat is doing a lot better."""
        outcome = [
            ('Cooperator', 90),
            ('Defector', 92),
            ('Grudger', 99),
            ('GoByMajority', 99),
            ('TitForTat', 99)]
        self.assertEqual(self.get_test_outcome(outcome), outcome)
