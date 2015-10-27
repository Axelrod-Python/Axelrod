import random
import unittest

import axelrod
from axelrod import simulate_play
from axelrod.strategy_transformers import *

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestTransformers(unittest.TestCase):

    def test_naming(self):
        """Tests that the player and class names are properly modified."""
        cls = FlipTransformer(axelrod.Cooperator)
        p1 = cls()
        self.assertEqual(cls.__name__, "FlippedCooperator")
        self.assertEqual(p1.name, "Flipped Cooperator")

    def test_cloning(self):
        """Tests that Player.clone preserves the application of transformations.
        """
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer(axelrod.Cooperator)() # Defector
        p3 = p2.clone()
        self.assertEqual(simulate_play(p1, p3), (C, D))
        self.assertEqual(simulate_play(p1, p3), (C, D))

    def test_generic(self):
        """Test that the generic wrapper does nothing."""
        transformer = StrategyTransformerFactory(generic_strategy_wrapper)()
        Cooperator2 = transformer(axelrod.Cooperator)
        p1 = Cooperator2()
        p2 = axelrod.Cooperator()
        self.assertEqual(simulate_play(p1, p2), (C, C))
        self.assertEqual(simulate_play(p1, p2), (C, C))

    def test_flip_transformer(self):
        """Tests that FlipTransformer(Cooperator) == Defector."""
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer(axelrod.Cooperator)() # Defector
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

    def test_cycler(self):
        """A test that demonstrates the difference in outcomes if
        FlipTransformer is applied to Alternator and CyclerCD."""
        # Difference between Alternator and CyclerCD
        p1 = axelrod.Cycler(cycle="CD")
        p2 = FlipTransformer(axelrod.Cycler)(cycle="CD")
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, D, C])
        self.assertEqual(p2.history, [D, C, D, C, D])

        p1 = axelrod.Alternator()
        p2 = FlipTransformer(axelrod.Alternator)()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, D, C])
        self.assertEqual(p2.history, [D, D, D, D, D])

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
        p2.tournament_attributes["length"] = 6
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
        p2 = TrackHistoryTransformer(axelrod.Random)()
        for _ in range(6):
            p1.play(p2)
        self.assertEqual(p2.history, p2._recorded_history)

    def test_composition(self):
        """Tests that transformations can be chained or composed."""
        cls1 = InitialTransformer([D, D])(axelrod.Cooperator)
        cls2 = FinalTransformer([D, D])(cls1)
        p1 = cls2()
        p2 = axelrod.Cooperator()
        p1.tournament_attributes["length"] = 8
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, C, C, C, C, D, D])

        cls1 = FinalTransformer([D, D])(InitialTransformer([D, D])(axelrod.Cooperator))
        p1 = cls1()
        p2 = axelrod.Cooperator()
        p1.tournament_attributes["length"] = 8
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, C, C, C, C, D, D])

    def test_retailiation(self):
        """Tests the RetailiateUntilApologyTransformer."""
        TFT = RetailiateUntilApologyTransformer(axelrod.Cooperator)
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



## Test that RUA(Cooperator) is the same as TitForTat
## reusing the TFT tests. Since TFT is completely specified by its tests,
## this is actually a proof that they are equal!
## However because classifier is a class variable until after instantiation
## this alters Cooperator's class variable, and causes its test to fail
## So for now this is commented out.

#RUA = RetailiateUntilApologyTransformer()
#TFT = RUA(axelrod.Cooperator)
#TFT.name = "Tit For Tat"
#TFT.classifier["memory_depth"] = 1

#class TestRUAisTFT(test_titfortat.TestTitForTat):
    ## This runs the 7 TFT tests when unittest is invoked
    #player = TFT

## Test that FlipTransformer(Defector) == Cooperator
#Cooperator2 = FlipTransformer(axelrod.Defector)
#Cooperator2.name = "Cooperator"
#Cooperator2.classifier["memory_depth"] = 0


#class TestFlipDefector(test_cooperator.TestCooperator):
    ## This runs the 7 TFT tests when unittest is invoked
    #player = Cooperator2
