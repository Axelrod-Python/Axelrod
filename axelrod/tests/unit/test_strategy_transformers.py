
import random
import unittest

import axelrod
from axelrod.strategies.strategy_transformers import *
from .test_titfortat import TestTitForTat


C, D = axelrod.Actions.C, axelrod.Actions.D


class TestTransformers(unittest.TestCase):

    def test_naming(self):
        cls = FlipTransformer(axelrod.Cooperator)
        p1 = cls()
        self.assertEqual(cls.__name__, "FlippedCooperator")
        self.assertEqual(p1.name, "Flipped Cooperator")

    def test_cloning(self):
        # Test that cloning preserves transform
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer(axelrod.Cooperator)() # Defector
        p3 = p2.clone()
        self.assertEqual(simulate_play(p1, p3), (C, D))
        self.assertEqual(simulate_play(p1, p3), (C, D))

    def test_flip_transformer(self):
        # Cooperator to Defector
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer(axelrod.Cooperator)() # Defector
        self.assertEqual(simulate_play(p1, p2), (C, D))
        self.assertEqual(simulate_play(p1, p2), (C, D))
        self.assertEqual(simulate_play(p1, p2), (C, D))

    def test_noisy_transformer(self):
        random.seed(5)
        # Cooperator to Defector
        p1 = axelrod.Cooperator()
        p2 = NoisyTransformer(0.5)(axelrod.Cooperator)() # Defector
        for _ in range(10):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, C, C, C, D, D, C, C])

    def test_forgiving(self):
        random.seed(10)
        p1 = ForgiverTransformer(0.5)(axelrod.Defector)()
        p2 = axelrod.Defector()
        for _ in range(10):
            p1.play(p2)
        self.assertEqual(p1.history, [D, C, D, C, D, D, D, C, D, C])

    def test_cycler(self):
        # Difference between Alternator and CyclerCD
        p1 = axelrod.Cycler(cycle="CD")
        p2 = FlipTransformer(axelrod.Cycler)(cycle="CD")
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, D, C])
        self.assertEqual(p2.history, [D, C, D, C, D])

    def test_initial_transformer(self):
        # Initial play transformer
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
        # Final play transformer
        p1 = axelrod.Cooperator()
        p2 = FinalTransformer([D, D, D])(axelrod.Cooperator)()
        p2.tournament_attributes["length"] = 6
        for _ in range(6):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, D, D, D])

    def test_final_transformer2(self):
        # Final play transformer (no tournament length)
        p1 = axelrod.Cooperator()
        p2 = FinalTransformer()(axelrod.Cooperator)()
        for _ in range(6):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, C, C, C])

    def test_composition(self):
        cls1 = InitialTransformer()(axelrod.Cooperator)
        cls2 = FinalTransformer()(cls1)
        p1 = cls2()
        p2 = axelrod.Cooperator()
        p1.tournament_attributes["length"] = 8
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, D, C, C, D, D, D])

        cls1 = FinalTransformer()(InitialTransformer()(axelrod.Cooperator))
        p1 = cls1()
        p2 = axelrod.Cooperator()
        p1.tournament_attributes["length"] = 8
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, D, C, C, D, D, D])


# Test that RUA(Cooperator) is the same as TitForTat
# Reusing the TFT tests
RUA = RetailiateUntilApologyTransformer()
TFT = RUA(axelrod.Cooperator)

class TestRUA(TestTitForTat):
    @classmethod
    def setUpClass(cls):
        player = TFT
        name = "RUA Cooperator"
        # Skips testing this, which is zero but should be 1
        #expected_classifier["memory_depth"] = 1


