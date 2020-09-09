import pickle
import unittest

import axelrod as axl

C, D = axl.Action.C, axl.Action.D
random = axl.RandomGenerator()

# A set of classes to test pickling.

# First set: special cases

PointerToWrappedStrategy = axl.strategy_transformers.FlipTransformer()(
    axl.strategy_transformers.FlipTransformer()(axl.Cooperator)
)


class MyDefector(axl.Player):
    def __init__(self):
        super(MyDefector, self).__init__()

    def strategy(self, opponent):
        return D


PointerToWrappedClassNotInStrategies = (
    axl.strategy_transformers.FlipTransformer()(
        axl.strategy_transformers.FlipTransformer()(MyDefector)
    )
)


@axl.strategy_transformers.InitialTransformer((D, C, D), name_prefix=None)
@axl.strategy_transformers.DualTransformer(name_prefix=None)
@axl.strategy_transformers.FlipTransformer(name_prefix=None)
@axl.strategy_transformers.DualTransformer(name_prefix=None)
class InterspersedDualTransformersNamePrefixAbsent(axl.Cooperator):
    pass


@axl.strategy_transformers.IdentityTransformer((D, D, C))
@axl.strategy_transformers.DualTransformer()
@axl.strategy_transformers.FlipTransformer()
@axl.strategy_transformers.DualTransformer()
class InterspersedDualTransformersNamePrefixPresent(axl.Cooperator):
    pass


@axl.strategy_transformers.FlipTransformer()
class MyCooperator(axl.Player):
    def strategy(self, opponent):
        return C


@axl.strategy_transformers.FlipTransformer()
@axl.strategy_transformers.FlipTransformer()
class DoubleFlip(axl.Cooperator):
    pass


@axl.strategy_transformers.FlipTransformer()
class SingleFlip(axl.Cooperator):
    pass


# Second set: All the transformers


@axl.strategy_transformers.ApologyTransformer([D], [C], name_prefix=None)
class Apology(axl.Cooperator):
    pass


@axl.strategy_transformers.DeadlockBreakingTransformer(name_prefix=None)
class DeadlockBreaking(axl.Cooperator):
    pass


@axl.strategy_transformers.DualTransformer(name_prefix=None)
class Dual(axl.Cooperator):
    pass


@axl.strategy_transformers.FlipTransformer(name_prefix=None)
class Flip(axl.Cooperator):
    pass


@axl.strategy_transformers.FinalTransformer((D, D), name_prefix=None)
class Final(axl.Cooperator):
    pass


@axl.strategy_transformers.ForgiverTransformer(0.2, name_prefix=None)
class Forgiver(axl.Cooperator):
    pass


@axl.strategy_transformers.GrudgeTransformer(3, name_prefix=None)
class Grudge(axl.Cooperator):
    pass


@axl.strategy_transformers.InitialTransformer((C, D), name_prefix=None)
class Initial(axl.Cooperator):
    pass


@axl.strategy_transformers.JossAnnTransformer((0.2, 0.2), name_prefix=None)
class JossAnn(axl.Cooperator):
    pass


strategies = [axl.Grudger, axl.TitForTat]
probability = [0.2, 0.3]


@axl.strategy_transformers.MixedTransformer(
    probability, strategies, name_prefix=None
)
class Mixed(axl.Cooperator):
    pass


@axl.strategy_transformers.NiceTransformer(name_prefix=None)
class Nice(axl.Cooperator):
    pass


@axl.strategy_transformers.NoisyTransformer(0.2, name_prefix=None)
class Noisy(axl.Cooperator):
    pass


@axl.strategy_transformers.RetaliationTransformer(3, name_prefix=None)
class Retaliation(axl.Cooperator):
    pass


@axl.strategy_transformers.RetaliateUntilApologyTransformer(name_prefix=None)
class RetaliateUntilApology(axl.Cooperator):
    pass


@axl.strategy_transformers.TrackHistoryTransformer(name_prefix=None)
class TrackHistory(axl.Cooperator):
    pass


@axl.strategy_transformers.IdentityTransformer()
class Identity(axl.Cooperator):
    pass


@axl.strategy_transformers.IdentityTransformer(name_prefix=None)
class TransformedThue(axl.ThueMorse):
    pass


class MetaThue(axl.MetaPlayer):
    name = "MetaThue"

    def __init__(self):
        team = [axl.ThueMorse]
        super().__init__(team=team)


TransformedMetaThue = axl.strategy_transformers.IdentityTransformer(
    name_prefix=None
)(MetaThue)


transformed_no_prefix = [
    Apology,
    DeadlockBreaking,
    Flip,
    Final,
    Forgiver,
    Grudge,
    Initial,
    JossAnn,
    Mixed,
    Nice,
    Noisy,
    Retaliation,
    RetaliateUntilApology,
    TrackHistory,
    Dual,
    Identity,
]

transformer_instances = [
    axl.strategy_transformers.ApologyTransformer([D], [C]),
    axl.strategy_transformers.DeadlockBreakingTransformer(),
    axl.strategy_transformers.DualTransformer(),
    axl.strategy_transformers.FlipTransformer(),
    axl.strategy_transformers.FinalTransformer((D, D)),
    axl.strategy_transformers.ForgiverTransformer(0.2),
    axl.strategy_transformers.GrudgeTransformer(3),
    axl.strategy_transformers.InitialTransformer((C, D)),
    axl.strategy_transformers.JossAnnTransformer((0.2, 0.6)),
    axl.strategy_transformers.MixedTransformer(probability, strategies),
    axl.strategy_transformers.NiceTransformer(),
    axl.strategy_transformers.NoisyTransformer(0.2),
    axl.strategy_transformers.RetaliationTransformer(3),
    axl.strategy_transformers.RetaliateUntilApologyTransformer(),
    axl.strategy_transformers.TrackHistoryTransformer(),
    axl.strategy_transformers.IdentityTransformer(),
]


class TestPickle(unittest.TestCase):
    def assert_equals_instance_from_pickling(self, original_instance):
        clone = pickle.loads(pickle.dumps(original_instance))
        self.assertEqual(clone, original_instance)

    def assert_original_equals_pickled(self, player_, turns=10):
        opponents = (axl.Defector, axl.Cooperator, axl.Random, axl.CyclerCCCDCD)
        for opponent_class in opponents:
            # Check that player and copy play the same way.
            player = player_.clone()
            clone = pickle.loads(pickle.dumps(player))
            clone = clone.clone()

            opponent_1 = opponent_class()
            opponent_2 = opponent_class()

            match_1 = axl.Match((player, opponent_1), turns=turns, seed=1)
            result_1 = match_1.play()

            match_2 = axl.Match((clone, opponent_2), turns=turns, seed=1)
            result_2 = match_2.play()

            self.assertEqual(result_1, result_2)

            # Confirm that mutated player can be pickled correctly.
            self.assert_equals_instance_from_pickling(player)

    def test_parameterized_player(self):
        player = axl.Cycler("DDCCDD")
        self.assert_original_equals_pickled(player)

    def test_sequence_player(self):
        inline_transformed_thue = axl.strategy_transformers.IdentityTransformer(
            name_prefix="Transformed"
        )(axl.ThueMorse)()
        for player in [
            axl.ThueMorse(),
            axl.ThueMorseInverse(),
            MetaThue(),
            TransformedMetaThue(),
            inline_transformed_thue,
            TransformedThue(),
        ]:
            self.assert_equals_instance_from_pickling(player)
            opponents = (
                axl.Defector,
                axl.Cooperator,
                axl.Random,
                axl.CyclerCCCDCD,
            )
            for opponent_class in opponents:
                player.reset()
                opponent = opponent_class()
                match_1 = axl.Match((player, opponent), turns=20, seed=10)
                _ = match_1.play()
                self.assert_equals_instance_from_pickling(player)

    def test_final_transformer_called(self):
        player = axl.Alexei()
        copy = pickle.loads(pickle.dumps(player))
        match = axl.Match((player, copy), turns=3)
        results = match.play()
        self.assertEqual(results, [(C, C), (C, C), (D, D)])

    def test_pickling_all_strategies(self):
        for s in random.choice(axl.strategies, 50):
            with self.subTest(strategy=s.name):
                self.assert_original_equals_pickled(s())

    def test_pickling_all_transformers_as_decorated_classes(self):
        for s in transformed_no_prefix:
            with self.subTest(strategy=s.name):
                player = s()
                self.assert_original_equals_pickled(player)

    def test_pickling_all_transformers_as_instance_called_on_a_class(self):
        for transformer in transformer_instances:
            with self.subTest(transformer=transformer):
                player = transformer(axl.Cooperator)()
                self.assert_original_equals_pickled(player)

    def test_created_on_the_spot_multiple_transformers(self):
        player_class = axl.strategy_transformers.FlipTransformer()(
            axl.Cooperator
        )
        player_class = axl.strategy_transformers.DualTransformer()(player_class)
        player = axl.strategy_transformers.FinalTransformer((C, D))(
            player_class
        )()

        self.assert_original_equals_pickled(player)

    def test_dual_transformer_regression_test(self):
        """DualTransformer has failed when there were multiple DualTransformers.
        It has also failed when DualTransformer was not the outermost
        transformer or when other transformers were between multiple
        DualTransformers."""
        player = InterspersedDualTransformersNamePrefixAbsent()
        self.assert_original_equals_pickled(player)

        player = InterspersedDualTransformersNamePrefixPresent()
        self.assert_original_equals_pickled(player)

        player_class = axl.WinStayLoseShift
        player_class = axl.strategy_transformers.DualTransformer()(player_class)
        player_class = axl.strategy_transformers.InitialTransformer((C, D))(
            player_class
        )
        player_class = axl.strategy_transformers.DualTransformer()(player_class)
        player_class = axl.strategy_transformers.TrackHistoryTransformer()(
            player_class
        )

        interspersed_dual_transformers = player_class()

        self.assert_original_equals_pickled(interspersed_dual_transformers)

    def test_class_and_instance_name_different_single_flip(self):
        player = SingleFlip()
        self.assertEqual(player.__class__.__name__, "FlippedSingleFlip")

        self.assert_original_equals_pickled(player)

    def test_class_and_instance_name_different_double_flip(self):
        player = DoubleFlip()
        self.assertEqual(player.__class__.__name__, "FlippedFlippedDoubleFlip")

        self.assert_original_equals_pickled(player)

    def test_class_and_instance_name_different_built_from_player_class(self):
        player = MyCooperator()
        class_names = [class_.__name__ for class_ in MyCooperator.mro()]
        self.assertEqual(
            class_names,
            ["FlippedMyCooperator", "MyCooperator", "Player", "object"],
        )

        self.assert_original_equals_pickled(player)

    def test_pointer_to_class_derived_from_strategy(self):
        player = PointerToWrappedStrategy()

        class_names = [class_.__name__ for class_ in player.__class__.mro()]
        self.assertEqual(
            class_names,
            [
                "FlippedFlippedCooperator",
                "FlippedCooperator",
                "Cooperator",
                "Player",
                "object",
            ],
        )

        self.assert_original_equals_pickled(player)

    def test_pointer_to_class_derived_from_Player(self):
        player = PointerToWrappedClassNotInStrategies()

        class_names = [class_.__name__ for class_ in player.__class__.mro()]
        self.assertEqual(
            class_names,
            [
                "FlippedFlippedMyDefector",
                "FlippedMyDefector",
                "MyDefector",
                "Player",
                "object",
            ],
        )

        self.assert_original_equals_pickled(player)

    def test_local_class_unpicklable(self):
        """An unpickle-able AND transformed class will not raise an error until
        it is un-pickled. This is different from the original class that raises
        an error when it is pickled."""

        class LocalCooperator(axl.Cooperator):
            pass

        un_transformed = LocalCooperator()

        self.assertRaises(AttributeError, pickle.dumps, un_transformed)

        player = axl.strategy_transformers.FlipTransformer()(LocalCooperator)()
        pickled = pickle.dumps(player)
        self.assertRaises(AttributeError, pickle.loads, pickled)

    def test_with_various_name_prefixes(self):
        no_prefix = Flip()
        self.assertEqual(no_prefix.__class__.__name__, "Flip")
        self.assert_original_equals_pickled(no_prefix)

        default_prefix = axl.strategy_transformers.FlipTransformer()(
            axl.Cooperator
        )()
        self.assertEqual(default_prefix.__class__.__name__, "FlippedCooperator")
        self.assert_original_equals_pickled(default_prefix)

        fliptastic = axl.strategy_transformers.FlipTransformer(
            name_prefix="Fliptastic"
        )
        new_prefix = fliptastic(axl.Cooperator)()
        self.assertEqual(new_prefix.__class__.__name__, "FliptasticCooperator")
        self.assert_original_equals_pickled(new_prefix)

    def test_dynamic_class_no_name_prefix(self):
        player = axl.strategy_transformers.FlipTransformer(name_prefix=None)(
            axl.Cooperator
        )()

        self.assertEqual(player.__class__.__name__, "Cooperator")
        self.assert_original_equals_pickled(player)
