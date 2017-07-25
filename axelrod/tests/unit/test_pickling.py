import pickle
import unittest

import axelrod as axl
from axelrod.strategy_transformers import FlipTransformer
from axelrod.tests.classes_for_testing_pickling import (transformed, DoubleFlip,
                                                        SingleFlip, MyCooperator,
                                                        VariableAsClassPointer,
                                                        Dual, Flip)

C, D = axl.Action.C, axl.Action.D


class TestPickle(unittest.TestCase):

    def assert_original_plays_same_as_pickled(self, player, turns=10):
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

    def assert_instance_with_history_equality(self, player):
        turns = 5
        opponent = axl.Alternator()
        for _ in range(turns):
            player.play(opponent)
        new = pickle.loads(pickle.dumps(player))
        self.assertEqual(player, new)

    def test_blah(self):
        player = Flip()
        orig = player.__class__.original_class()

        self.assertEqual(player.strategy(axl.Cooperator()), D)
        self.assertEqual(orig.strategy(axl.Cooperator()), C)

        player = pickle.loads(pickle.dumps(player))
        orig = player.__class__.original_class()

        self.assertEqual(player.strategy(axl.Cooperator()), D)
        self.assertEqual(orig.strategy(axl.Cooperator()), C)

    def test_parameterized_player(self):
        player = axl.Cycler('DDCCDD')
        self.assert_instance_with_history_equality(player)

    def test_sequence_player(self):
        player = axl.ThueMorse()
        self.assert_instance_with_history_equality(player)

    def test_final_transformer_called(self):
        player = axl.Alexei()
        copy = pickle.loads(pickle.dumps(player))
        match = axl.Match((player, copy), turns=3)
        results = match.play()
        self.assertEqual(results, [(C, C), (C, C), (D, D)])

        self.assert_original_plays_same_as_pickled(axl.Alexei(), turns=10)

    def test_nice_transformer_class(self):
        player = axl.NMWEDeterministic()
        self.assert_original_plays_same_as_pickled(player, turns=10)

    def test_all(self):
        for s in axl.strategies:
            player = s()
            player.play(axl.Cooperator())
            reconstituted = pickle.loads(pickle.dumps(player))
            self.assertEqual(reconstituted, player)

    def test_pickling_transformers(self):

        for s in transformed:
            player = s()
            self.assert_instance_with_history_equality(player)
            # player.play(axl.Cooperator())
            # reconstituted = pickle.loads(pickle.dumps(player))
            # self.assertEqual(reconstituted, player)

    def test_created_on_the_spot(self):
        x = FlipTransformer()(axl.Cooperator)
        x = FlipTransformer()(x)
        x = FlipTransformer()(x)()
        z = pickle.loads(pickle.dumps(x))

        self.assertEqual(x, z)

    def test_class_and_instance_name_different_single_flip(self):
        player = SingleFlip()
        self.assertEqual(player.__class__.__name__, 'FlippedSingleFlip')

        self.assert_instance_with_history_equality(player)
        self.assert_original_plays_same_as_pickled(player, turns=10)

    def test_class_and_instance_name_different_double_flip(self):
        player = DoubleFlip()
        self.assertEqual(player.__class__.__name__, 'FlippedFlippedDoubleFlip')

        self.assert_instance_with_history_equality(player)
        self.assert_original_plays_same_as_pickled(player, turns=10)

    def test_class_and_instance_name_different_built_from_player_class(self):
        player = MyCooperator()
        class_names = [klass.__name__ for klass in MyCooperator.mro()]
        self.assertEqual(
            class_names,
            ['FlippedMyCooperator', 'MyCooperator', 'Player', 'object']
        )

        self.assert_original_plays_same_as_pickled(player, turns=10)
        self.assert_instance_with_history_equality(player)

    def test_pointer_to_made_class(self):
        player = VariableAsClassPointer()
        self.assertEqual(player.__class__.__name__, 'FlippedFlippedCooperator')
