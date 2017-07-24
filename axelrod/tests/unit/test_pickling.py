import pickle
import unittest

import axelrod as axl
from axelrod.strategy_transformers import FlipTransformer
from axelrod.tests.classes_for_testing_pickling import transformed, DoubleFlip

C, D = axl.Action.C, axl.Action.D


class TestPickle(unittest.TestCase):

    def assert_original_acts_same_as_pickled(self, player, turns=100):
        copy = pickle.loads(pickle.dumps(player))
        opponent_1 = axl.CyclerCCCDCD()
        opponent_2 = axl.CyclerCCCDCD()
        axl.seed(0)
        match_1 = axl.Match((player, opponent_1), turns=turns)
        result_1 = match_1.play()

        axl.seed(0)
        match_2 = axl.Match((copy, opponent_2), turns=turns)
        result_2 = match_2.play()

        self.assertEqual(result_1, result_2)

    def test_parameterized_player(self):
        p1 = axl.Cooperator()
        p2 = axl.Cycler('DDCCDD')

        p1.play(p2)

        reconstituted_1 = pickle.loads(pickle.dumps(p1))
        reconstituted_2 = pickle.loads(pickle.dumps(p2))

        self.assertEqual(p2, reconstituted_2)

        self.assertEqual(reconstituted_1.clone(), p1.clone())
        self.assertEqual(reconstituted_2.clone(), p2.clone())

    def test_sequence_player(self):
        player = axl.ThueMorse()
        player.play(axl.Cooperator())

        reconstituted = pickle.loads(pickle.dumps(player))
        self.assertEqual(reconstituted, player)

    def test_final_transformer_called(self):
        player = axl.Alexei()
        copy = pickle.loads(pickle.dumps(player))
        match = axl.Match((player, copy), turns=3)
        results = match.play()
        self.assertEqual(results, [(C, C), (C, C), (D, D)])

        self.assert_original_acts_same_as_pickled(axl.Alexei(), turns=10)

    def test_nice_transformer_called(self):
        player = axl.NMWEDeterministic()
        self.assert_original_acts_same_as_pickled(player, turns=10)

    def test_all(self):
        for s in axl.strategies:
            player = s()
            player.play(axl.Cooperator())

            reconstituted = pickle.loads(pickle.dumps(player))

            self.assertEqual(reconstituted, player)

    def test_pickling_transformers(self):

        for s in transformed:
            player = s()
            player.play(axl.Cooperator())
            reconstituted = pickle.loads(pickle.dumps(player))
            self.assertEqual(reconstituted, player)

    def test_created(self):
        x = FlipTransformer()(axl.Cooperator)
        x = FlipTransformer()(x)
        x = FlipTransformer()(x)()
        z = pickle.loads(pickle.dumps(x))

        self.assertEqual(x, z)

    def test_created_two(self):
        x = DoubleFlip()
        z = pickle.dumps(x)
        self.assertEqual(x, pickle.loads(z))
        self.assert_original_acts_same_as_pickled(x, turns=10)
