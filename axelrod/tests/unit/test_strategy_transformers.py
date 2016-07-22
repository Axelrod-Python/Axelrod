import random
import unittest

import axelrod
from axelrod import simulate_play
from axelrod.strategy_transformers import *
from .test_titfortat import TestTitForTat
from .test_cooperator import TestCooperator

C, D = axelrod.Actions.C, axelrod.Actions.D

@IdentityTransformer
class TestClass(object):
    name = 'Test Class'


class TestTransformers(unittest.TestCase):

    def test_all_strategies(self):
        # Attempt to transform each strategy to ensure that implementation
        # choices (like use of super) do not cause issues
        for s in axelrod.strategies:
            opponent = axelrod.Cooperator()
            player = IdentityTransformer()(s)()
            player.play(opponent)

    def test_naming(self):
        """Tests that the player and class names are properly modified."""
        cls = FlipTransformer()(axelrod.Cooperator)
        p1 = cls()
        self.assertEqual(cls.__name__, "FlippedCooperator")
        self.assertEqual(p1.name, "Flipped Cooperator")

        cls = ForgiverTransformer(0.5)(axelrod.Alternator)
        p1 = cls()
        self.assertEqual(cls.__name__, "ForgivingAlternator")
        self.assertEqual(p1.name, "Forgiving Alternator")

        cls = ForgiverTransformer(0.5, name_prefix="")(axelrod.Alternator)
        p1 = cls()
        self.assertEqual(cls.__name__, "Alternator")
        self.assertEqual(p1.name, "Alternator")

    def test_cloning(self):
        """Tests that Player.clone preserves the application of transformations.
        """
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer()(axelrod.Cooperator)() # Defector
        p3 = p2.clone()
        self.assertEqual(simulate_play(p1, p3), (C, D))
        self.assertEqual(simulate_play(p1, p3), (C, D))

    def test_generic(self):
        """Test that the generic wrapper does nothing."""
        # This is the identity transformer
        transformer = StrategyTransformerFactory(generic_strategy_wrapper)()
        Cooperator2 = transformer(axelrod.Cooperator)
        p1 = Cooperator2()
        p2 = axelrod.Cooperator()
        self.assertEqual(simulate_play(p1, p2), (C, C))
        self.assertEqual(simulate_play(p1, p2), (C, C))

    def test_flip_transformer(self):
        """Tests that FlipTransformer(Cooperator) == Defector."""
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer()(axelrod.Cooperator)() # Defector
        self.assertEqual(simulate_play(p1, p2), (C, D))
        self.assertEqual(simulate_play(p1, p2), (C, D))
        self.assertEqual(simulate_play(p1, p2), (C, D))

    def test_noisy_transformer(self):
        """Tests that the noisy transformed does flip some moves."""
        random.seed(5)
        # Cooperator to Defector
        p1 = axelrod.Cooperator()
        p2 = NoisyTransformer(0.5)(axelrod.Cooperator)()
        for _ in range(10):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, C, C, C, D, D, C, C])

    def test_forgiving(self):
        """Tests that the forgiving transformer flips some defections."""
        random.seed(10)
        p1 = ForgiverTransformer(0.5)(axelrod.Alternator)()
        p2 = axelrod.Defector()
        for _ in range(10):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, C, D, C, C, D, C, D])

    def test_initial_transformer(self):
        """Tests the InitialTransformer."""
        p1 = axelrod.Cooperator()
        p2 = InitialTransformer([D, D])(axelrod.Cooperator)()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p2.history, [D, D, C, C, C])

        p1 = axelrod.Cooperator()
        p2 = InitialTransformer([D, D, C, D])(axelrod.Cooperator)()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p2.history, [D, D, C, D, C])

    def test_final_transformer(self):
        """Tests the FinalTransformer when tournament length is known."""
        # Final play transformer
        p1 = axelrod.Cooperator()
        p2 = FinalTransformer([D, D, D])(axelrod.Cooperator)()
        p2.match_attributes["length"] = 6
        for _ in range(6):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, D, D, D])

    def test_final_transformer2(self):
        """Tests the FinalTransformer when tournament length is not known."""
        p1 = axelrod.Cooperator()
        p2 = FinalTransformer([D, D])(axelrod.Cooperator)()
        for _ in range(6):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, C, C, C])

    def test_history_track(self):
        """Tests the history tracking transformer."""
        p1 = axelrod.Cooperator()
        p2 = TrackHistoryTransformer()(axelrod.Random)()
        for _ in range(6):
            p1.play(p2)
        self.assertEqual(p2.history, p2._recorded_history)

    def test_composition(self):
        """Tests that transformations can be chained or composed."""
        cls1 = InitialTransformer([D, D])(axelrod.Cooperator)
        cls2 = FinalTransformer([D, D])(cls1)
        p1 = cls2()
        p2 = axelrod.Cooperator()
        p1.match_attributes["length"] = 8
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, C, C, C, C, D, D])

        cls1 = FinalTransformer([D, D])(InitialTransformer([D, D])(axelrod.Cooperator))
        p1 = cls1()
        p2 = axelrod.Cooperator()
        p1.match_attributes["length"] = 8
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, C, C, C, C, D, D])

    def test_compose_transformers(self):
        cls1 = compose_transformers(FinalTransformer([D, D]), InitialTransformer([D, D]))
        p1 = cls1(axelrod.Cooperator)()
        p2 = axelrod.Cooperator()
        p1.match_attributes["length"] = 8
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, C, C, C, C, D, D])

    def test_retailiation(self):
        """Tests the RetaliateTransformer."""
        p1 = RetaliationTransformer(1)(axelrod.Cooperator)()
        p2 = axelrod.Defector()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, D, D, D])
        self.assertEqual(p2.history, [D, D, D, D, D])

        p1 = RetaliationTransformer(1)(axelrod.Cooperator)()
        p2 = axelrod.Alternator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, D, C, D])
        self.assertEqual(p2.history, [C, D, C, D, C])

        TwoTitsForTat = RetaliationTransformer(2)(axelrod.Cooperator)
        p1 = TwoTitsForTat()
        p2 = axelrod.CyclerCCD()
        for _ in range(9):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, C, D, D, C, D, D, C])
        self.assertEqual(p2.history, [C, C, D, C, C, D, C, C, D])

    def test_retaliation_until_apology(self):
        """Tests the RetaliateUntilApologyTransformer."""
        TFT = RetaliateUntilApologyTransformer()(axelrod.Cooperator)
        p1 = TFT()
        p2 = axelrod.Cooperator()
        p1.play(p2)
        p1.play(p2)
        self.assertEqual(p1.history, [C, C])

        p1 = TFT()
        p2 = axelrod.Defector()
        p1.play(p2)
        p1.play(p2)
        self.assertEqual(p1.history, [C, D])

        random.seed(12)
        p1 = TFT()
        p2 = axelrod.Random()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, D, D, C])

    def test_apology(self):
        """Tests the ApologyTransformer."""
        ApologizingDefector = ApologyTransformer([D], [C])(axelrod.Defector)
        p1 = ApologizingDefector()
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [D, C, D, C, D])
        ApologizingDefector = ApologyTransformer([D, D], [C, C])(axelrod.Defector)
        p1 = ApologizingDefector()
        p2 = axelrod.Cooperator()
        for _ in range(6):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, C, D, D, C])

    def test_mixed(self):
        """Tests the MixedTransformer."""
        probability = 1
        MD = MixedTransformer(probability, axelrod.Cooperator)(axelrod.Defector)

        p1 = MD()
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, C, C, C])

        probability = 0
        MD = MixedTransformer(probability, axelrod.Cooperator)(axelrod.Defector)

        p1 = MD()
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, D, D, D])

        # Decorating with list and distribution

        # Decorate a cooperator putting all weight on other strategies that are
        # 'nice'
        probability = [.3, .2, 0]
        strategies = [axelrod.TitForTat, axelrod.Grudger, axelrod.Defector]
        MD = MixedTransformer(probability, strategies)(axelrod.Cooperator)

        p1 = MD()
        # Against a cooperator we see that we only cooperate
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, C, C, C])

        # Decorate a cooperator putting all weight on Defector
        probability = (0, 0, 1)  # Note can also pass tuple
        strategies = [axelrod.TitForTat, axelrod.Grudger, axelrod.Defector]
        MD = MixedTransformer(probability, strategies)(axelrod.Cooperator)

        p1 = MD()
        # Against a cooperator we see that we only cooperate
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, D, D, D])

    def test_deadlock(self):
        """Test the DeadlockBreakingTransformer."""
        # We can induce a deadlock by alterting TFT to defect first
        p1 = axelrod.TitForTat()
        p2 = InitialTransformer([D])(axelrod.TitForTat)()
        for _ in range(4):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, D])
        self.assertEqual(p2.history, [D, C, D, C])

        # Now let's use the transformer to break the deadlock to achieve
        # Mutual cooperation
        p1 = axelrod.TitForTat()
        p2 = DeadlockBreakingTransformer()(InitialTransformer([D])(axelrod.TitForTat))()
        for _ in range(4):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, C])
        self.assertEqual(p2.history, [D, C, C, C])

    def test_grudging(self):
        """Test the GrudgeTransformer."""
        p1 = axelrod.Defector()
        p2 = GrudgeTransformer(1)(axelrod.Cooperator)()
        for _ in range(4):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, D, D])
        self.assertEqual(p2.history, [C, C, D, D])

        p1 = InitialTransformer([C])(axelrod.Defector)()
        p2 = GrudgeTransformer(2)(axelrod.Cooperator)()
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, D, D, D, D, D, D])
        self.assertEqual(p2.history, [C, C, C, C, D, D, D, D])

    def test_nilpotency(self):
        """Show that some of the transformers are (sometimes) nilpotent, i.e.
        that transfomer(transformer(PlayerClass)) == PlayerClass"""
        for transformer in [IdentityTransformer(),
                            FlipTransformer(),
                            TrackHistoryTransformer()]:
            for PlayerClass in [axelrod.Cooperator, axelrod.Defector]:
                for third_player in [axelrod.Cooperator(), axelrod.Defector()]:
                    player = PlayerClass()
                    transformed = transformer(transformer(PlayerClass))()
                    for _ in range(5):
                        self.assertEqual(player.strategy(third_player),
                                        transformed.strategy(third_player))
                        player.play(third_player)
                        third_player.history.pop(-1)
                        transformed.play(third_player)

    def test_idempotency(self):
        """Show that these transformers are idempotent, i.e. that
        transfomer(transformer(PlayerClass)) == transformer(PlayerClass).
        That means that the transformer is a projection on the set of
        strategies."""
        for transformer in [IdentityTransformer(), GrudgeTransformer(1),
                            FinalTransformer([C]), FinalTransformer([D]),
                            InitialTransformer([C]), InitialTransformer([D]),
                            DeadlockBreakingTransformer(),
                            RetaliationTransformer(1),
                            RetaliateUntilApologyTransformer(),
                            TrackHistoryTransformer(),
                            ApologyTransformer([D], [C])]:
            for PlayerClass in [axelrod.Cooperator, axelrod.Defector]:
                for third_player in [axelrod.Cooperator(), axelrod.Defector()]:
                    player = transformer(PlayerClass)()
                    transformed = transformer(transformer(PlayerClass))()
                    for i in range(5):
                        self.assertEqual(player.strategy(third_player),
                                        transformed.strategy(third_player))
                        player.play(third_player)
                        third_player.history.pop(-1)
                        transformed.play(third_player)

    def test_implementation(self):
        """A test that demonstrates the difference in outcomes if
        FlipTransformer is applied to Alternator and CyclerCD. In other words,
        the implementation matters, not just the outcomes."""
        # Difference between Alternator and CyclerCD
        p1 = axelrod.Cycler(cycle="CD")
        p2 = FlipTransformer()(axelrod.Cycler)(cycle="CD")
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, D, C])
        self.assertEqual(p2.history, [D, C, D, C, D])

        p1 = axelrod.Alternator()
        p2 = FlipTransformer()(axelrod.Alternator)()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, D, C])
        self.assertEqual(p2.history, [D, D, D, D, D])


# Test that RUA(Cooperator) is the same as TitForTat
# reusing the TFT tests. Since TFT is completely specified by its tests,
# this is actually a proof that they are equal!
# However because classifier is a class variable until after instantiation
# this alters Cooperator's class variable, and causes its test to fail
# So for now this is commented out.

TFT = RetaliateUntilApologyTransformer()(axelrod.Cooperator)

class TestRUAisTFT(TestTitForTat):
    # This runs the 7 TFT tests when unittest is invoked
    player = TFT
    name = "RUA Cooperator"
    expected_classifier = {
        'memory_depth': 0, # really 1
        'stochastic': False,
        'makes_use_of': set(),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

# Test that FlipTransformer(Defector) == Cooperator
Cooperator2 = FlipTransformer()(axelrod.Defector)

class TestFlipDefector(TestCooperator):
    # This runs the 7 TFT tests when unittest is invoked
    name = "Flipped Defector"
    player = Cooperator2
