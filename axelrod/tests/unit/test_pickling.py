import pickle
import unittest

import axelrod as axl
import axelrod.strategy_transformers as st


C, D = axl.Action.C, axl.Action.D


# A set of classes to test pickling.

# First set: special cases

PointerToWrappedStrategy = st.FlipTransformer()(
    st.FlipTransformer()(axl.Cooperator)
)


class MyDefector(axl.Player):
    def __init__(self):
        super(MyDefector, self).__init__()

    def strategy(self, opponent):
        return D


PointerToWrappedClassNotInStrategies = st.FlipTransformer()(
    st.FlipTransformer()(MyDefector)
)


@st.IdentityTransformer()
@st.DualTransformer(name_prefix=None)
@st.FlipTransformer(name_prefix=None)
@st.DualTransformer(name_prefix=None)
class TestDualTransformerIssues(axl.Cooperator):
    pass


@st.IdentityTransformer()
@st.DualTransformer()
@st.FlipTransformer()
@st.DualTransformer()
class TestDualTransformerIssues2(axl.Cooperator):
    pass


@st.FlipTransformer()
class MyCooperator(axl.Player):
    def strategy(self, opponent):
        return C


@st.FlipTransformer()
@st.FlipTransformer()
class DoubleFlip(axl.Cooperator):
    pass


@st.FlipTransformer()
class SingleFlip(axl.Cooperator):
    pass


# Second set: All the transformers

@st.ApologyTransformer([D], [C], name_prefix=None)
class Apology(axl.Cooperator):
    pass


@st.DeadlockBreakingTransformer(name_prefix=None)
class DeadlockBreaking(axl.Cooperator):
    pass


@st.DualTransformer(name_prefix=None)
class Dual(axl.Cooperator):
    pass


@st.FlipTransformer(name_prefix=None)
class Flip(axl.Cooperator):
    pass


@st.FinalTransformer((D, D), name_prefix=None)
class Final(axl.Cooperator):
    pass


@st.ForgiverTransformer(0.2, name_prefix=None)
class Forgiver(axl.Cooperator):
    pass


@st.GrudgeTransformer(3, name_prefix=None)
class Grudge(axl.Cooperator):
    pass


@st.InitialTransformer((C, D), name_prefix=None)
class Initial(axl.Cooperator):
    pass


@st.JossAnnTransformer((0.2, 0.2), name_prefix=None)
class JossAnn(axl.Cooperator):
    pass


strategies = [axl.Grudger, axl.TitForTat]
probability = [.2, .3]


@st.MixedTransformer(probability, strategies, name_prefix=None)
class Mixed(axl.Cooperator):
    pass


@st.NiceTransformer(name_prefix=None)
class Nice(axl.Cooperator):
    pass


@st.NoisyTransformer(0.2, name_prefix=None)
class Noisy(axl.Cooperator):
    pass


@st.RetaliationTransformer(3, name_prefix=None)
class Retaliation(axl.Cooperator):
    pass


@st.RetaliateUntilApologyTransformer(name_prefix=None)
class RetaliateUntilApology(axl.Cooperator):
    pass


@st.TrackHistoryTransformer(name_prefix=None)
class TrackHistory(axl.Cooperator):
    pass

@st.IdentityTransformer()
class Identity(axl.Cooperator):
    pass

transformed_no_prefix = [Apology, DeadlockBreaking, Flip, Final, Forgiver,
                         Grudge, Initial, JossAnn, Mixed, Nice, Noisy,
                         Retaliation, RetaliateUntilApology, TrackHistory, Dual,
                         Identity]

transformer_instances = [
    st.ApologyTransformer([D], [C]),
    st.DeadlockBreakingTransformer(),
    st.DualTransformer(),
    st.FlipTransformer(),
    st.FinalTransformer((D, D)),
    st.ForgiverTransformer(0.2),
    st.GrudgeTransformer(3),
    st.InitialTransformer((C, D)),
    st.JossAnnTransformer((0.2, 0.6)),
    st.MixedTransformer(probability, strategies),
    st.NiceTransformer(),
    st.NoisyTransformer(0.2),
    st.RetaliationTransformer(3),
    st.RetaliateUntilApologyTransformer(),
    st.TrackHistoryTransformer(),
    st.IdentityTransformer()
]


class TestPickle(unittest.TestCase):

    def assert_orignal_equals_pickled(self, player, turns=10):
        self.assert_original_plays_same_as_pickled(player, turns)
        self.assert_mutated_instance_same_as_pickled(player)

    def assert_original_plays_same_as_pickled(self, player, turns=10):
        player.reset()
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

    def assert_mutated_instance_same_as_pickled(self, player):
        player.reset()
        turns = 5
        opponent = axl.Alternator()
        for _ in range(turns):
            player.play(opponent)
        new = pickle.loads(pickle.dumps(player))
        self.assertEqual(player, new)

    def test_parameterized_player(self):
        player = axl.Cycler('DDCCDD')
        self.assert_orignal_equals_pickled(player)

    def test_sequence_player(self):
        player = axl.ThueMorse()
        self.assert_orignal_equals_pickled(player)

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

    def test_pickling_all_strategies(self):
        for s in axl.strategies:
            self.assert_orignal_equals_pickled(s())

    def test_pickling_all_transformers_as_decorated_classes(self):
        for s in transformed_no_prefix:
            player = s()
            self.assert_orignal_equals_pickled(player)

    def test_pickling_all_transformers_as_instance_called_on_a_class(self):
        for transformer in transformer_instances:
            player = transformer(axl.Cooperator)()
            self.assert_orignal_equals_pickled(player)

    def test_created_on_the_spot_multiple_transformers(self):
        klass = st.FlipTransformer()(axl.Cooperator)
        klass = st.DualTransformer()(klass)
        player = st.FinalTransformer((C, D))(klass)()

        self.assert_orignal_equals_pickled(player)

    def test_dual_transformer_special_case(self):
        player = TestDualTransformerIssues()
        self.assert_orignal_equals_pickled(player)

        player = TestDualTransformerIssues2()
        self.assert_orignal_equals_pickled(player)

    def test_class_and_instance_name_different_single_flip(self):
        player = SingleFlip()
        self.assertEqual(player.__class__.__name__, 'FlippedSingleFlip')

        self.assert_orignal_equals_pickled(player)

    def test_class_and_instance_name_different_double_flip(self):
        player = DoubleFlip()
        self.assertEqual(player.__class__.__name__, 'FlippedFlippedDoubleFlip')

        self.assert_orignal_equals_pickled(player)

    def test_class_and_instance_name_different_built_from_player_class(self):
        player = MyCooperator()
        class_names = [klass.__name__ for klass in MyCooperator.mro()]
        self.assertEqual(
            class_names,
            ['FlippedMyCooperator', 'MyCooperator', 'Player', 'object']
        )

        self.assert_orignal_equals_pickled(player)

    def test_pointer_to_class_derived_from_strategy(self):
        player = PointerToWrappedStrategy()

        class_names = [klass.__name__ for klass in player.__class__.mro()]
        self.assertEqual(
            class_names,
            ['FlippedFlippedCooperator', 'FlippedCooperator', 'Cooperator',
             'Player', 'object']
        )

        self.assert_orignal_equals_pickled(player)

    def test_pointer_to_class_derived_from_Player(self):
        player = PointerToWrappedClassNotInStrategies()

        class_names = [klass.__name__ for klass in player.__class__.mro()]
        self.assertEqual(
            class_names,
            ['FlippedFlippedMyDefector', 'FlippedMyDefector', 'MyDefector',
             'Player', 'object']
        )

        self.assert_orignal_equals_pickled(player)

    def test_local_class_unpicklable(self):
        """An unpickle-able AND transformed class will not raise an error until
        it is un-pickled. This is different from the original class that raises
        an error when it is pickled."""

        class LocalCooperator(axl.Cooperator):
            pass

        un_transformed = LocalCooperator()

        self.assertRaises(AttributeError, pickle.dumps, un_transformed)

        player = st.FlipTransformer()(LocalCooperator)()
        pickled = pickle.dumps(player)
        self.assertRaises(AttributeError, pickle.loads, pickled)

    def test_with_various_name_prefixes(self):
        no_prefix = Flip()
        self.assertEqual(no_prefix.__class__.__name__, 'Flip')
        self.assert_orignal_equals_pickled(no_prefix)

        default_prefix = st.FlipTransformer()(axl.Cooperator)()
        self.assertEqual(default_prefix.__class__.__name__,
                         'FlippedCooperator')
        self.assert_orignal_equals_pickled(default_prefix)

        fliptastic = st.FlipTransformer(name_prefix='Fliptastic')
        new_prefix = fliptastic(axl.Cooperator)()
        self.assertEqual(new_prefix.__class__.__name__,
                         'FliptasticCooperator')
        self.assert_orignal_equals_pickled(new_prefix)

    def test_dynamic_class_no_name_prefix(self):
        player = st.FlipTransformer(name_prefix=None)(axl.Cooperator)()

        self.assertEqual(player.__class__.__name__, 'Cooperator')
        self.assert_orignal_equals_pickled(player)

