import unittest

import axelrod
from axelrod.strategy_transformers import *
from axelrod.tests.strategies.test_titfortat import TestTitForTat
from axelrod.tests.strategies.test_cooperator import TestCooperator

C, D = axelrod.Action.C, axelrod.Action.D


@FlipTransformer(name_prefix=None)
class CanPickle(axelrod.Cooperator):
    pass


@FlipTransformer()
class CanNotPickle(axelrod.Cooperator):
    pass


class TestTransformers(unittest.TestCase):

    def test_player_can_be_pickled(self):
        player = axelrod.Cooperator()
        self.assertTrue(player_can_be_pickled(player))

        player = IdentityTransformer()(axelrod.Cooperator)()
        self.assertFalse(player_can_be_pickled(player))

        player = CanPickle()
        self.assertTrue(player_can_be_pickled(player))

        player = CanNotPickle()
        self.assertFalse(player_can_be_pickled(player))

    def test_is_strategy_static(self):
        self.assertTrue(is_strategy_static(axelrod.Cooperator))
        self.assertFalse(is_strategy_static(axelrod.Alternator))

    def test_is_strategy_static_with_inherited_strategy(self):
        class NewCooperator(axelrod.Cooperator):
            pass

        class NewAlternator(axelrod.Alternator):
            pass

        self.assertTrue(is_strategy_static(NewCooperator))
        self.assertFalse(is_strategy_static(NewAlternator))

    def test_DecoratorReBuilder(self):
        new_prefix = 'YOLO'
        decorator = NoisyTransformer(0.2, name_prefix=new_prefix)

        factory_args = (noisy_wrapper, "Noisy", noisy_reclassifier)
        args = decorator.args
        kwargs = decorator.kwargs.copy()

        new_decorator = DecoratorReBuilder()(factory_args, args, kwargs,
                                             new_prefix)

        self.assertEqual(decorator(axelrod.Cooperator)(),
                         new_decorator(axelrod.Cooperator)())

    def test_StrategyReBuilder_declared_class_with_name_prefix(self):
        player = CanNotPickle()
        self.assertEqual(player.__class__.__name__, 'FlippedCanNotPickle')

        decorators = [player.decorator]
        import_name = 'CanNotPickle'
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

    def test_StrategyReBuilder_dynamically_wrapped_class_with_name_prefix(self):
        player = FlipTransformer()(axelrod.Cooperator)()
        self.assertEqual(player.__class__.__name__, 'FlippedCooperator')

        decorators = [player.decorator]
        import_name = 'Cooperator'
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

    def test_StrategyReBuilder_dynamically_wrapped_class_no_name_prefix(self):
        player = IdentityTransformer()(axelrod.Cooperator)()
        self.assertEqual(player.__class__.__name__, 'Cooperator')

        decorators = [player.decorator]
        import_name = 'Cooperator'
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

    def test_StrategyReBuilder_many_decorators(self):
        decorator_1 = IdentityTransformer()
        decorator_2 = FlipTransformer()
        decorator_3 = DualTransformer()
        player = decorator_3(decorator_2(decorator_1(axelrod.Cooperator)))()
        self.assertEqual(player.__class__.__name__,
                         'DualFlippedCooperator')

        decorators = [decorator_1, decorator_2, decorator_3]
        import_name = 'Cooperator'
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

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

    def test_repr(self):
        """Tests that the player __repr__ is properly modified to add
        Transformer's parameters.
        """
        self.assertEqual(str(ForgiverTransformer(0.5)(axelrod.Alternator)()), "Forgiving Alternator: 0.5")
        self.assertEqual(str(InitialTransformer([D, D, C])(axelrod.Alternator)()),
                         "Initial Alternator: [D, D, C]")
        self.assertEqual(str(FlipTransformer()(axelrod.Random)(0.1)), "Flipped Random: 0.1")
        self.assertEqual(str(MixedTransformer(0.3, (axelrod.Alternator, axelrod.Bully))(axelrod.Random)(0.1)),
                         "Mutated Random: 0.1: 0.3, ['Alternator', 'Bully']")

    def test_doc(self):
        """Test that the original docstring is present"""
        player = axelrod.Alternator()
        transformer = InitialTransformer([D, D, C])(axelrod.Alternator)()
        self.assertEqual(player.__doc__, transformer.__doc__)

    def test_cloning(self):
        """Tests that Player.clone preserves the application of transformations.
        """
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer()(axelrod.Cooperator)()  # Defector
        p3 = p2.clone()
        match = axelrod.Match((p1, p3), turns=2)
        results = match.play()
        self.assertEqual(results, [(C, D), (C, D)])

    def test_generic(self):
        """Test that the generic wrapper does nothing."""
        # This is the identity transformer
        transformer = StrategyTransformerFactory(generic_strategy_wrapper)()
        Cooperator2 = transformer(axelrod.Cooperator)
        p1 = Cooperator2()
        p2 = axelrod.Cooperator()
        match = axelrod.Match((p1, p2), turns=2)
        results = match.play()
        self.assertEqual(results, [(C, C), (C, C)])

    def test_flip_transformer(self):
        """Tests that FlipTransformer(Cooperator) == Defector."""
        p1 = axelrod.Cooperator()
        p2 = FlipTransformer()(axelrod.Cooperator)()  # Defector
        match = axelrod.Match((p1, p2), turns=3)
        results = match.play()
        self.assertEqual(results, [(C, D), (C, D), (C, D)])

    def test_flip_history(self):
        player = axelrod.Alternator()
        opponent = axelrod.Cooperator()
        for _ in range(5):
            player.play(opponent)

        self.assertEqual(player.history, [C, D, C, D, C])
        flip_history(player)
        self.assertEqual(player.history, [D, C, D, C, D])

    def test_switch_cooperations_and_defections(self):
        player = axelrod.Alternator()
        opponent = axelrod.Cooperator()
        for _ in range(5):
            player.play(opponent)

        self.assertEqual(player.cooperations, 3)
        self.assertEqual(player.defections, 2)
        switch_cooperations_and_defections(player)
        self.assertEqual(player.cooperations, 2)
        self.assertEqual(player.defections, 3)

    def test_flip_state_distribution(self):
        player = axelrod.Alternator()
        opponent = axelrod.CyclerCCD()
        for _ in range(16):
            player.play(opponent)

        expected = defaultdict(
            int, {(C, C): 5, (D, C): 6, (C, D): 3, (D, D): 2}
        )
        self.assertEqual(player.state_distribution, expected)

        flip_state_distribution(player)

        flip_expected = defaultdict(
            int, {(D, C): 5, (C, C): 6, (D, D): 3, (C, D): 2}
        )
        self.assertEqual(player.state_distribution, flip_expected)

    def test_flip_play_attributes(self):
        p1 = axelrod.WinStayLoseShift()
        p2 = DualTransformer()(axelrod.WinStayLoseShift)()
        p3 = axelrod.CyclerCCD()

        for _ in range(10):
            p1.play(p3)

        p3.reset()
        for _ in range(10):
            p2.play(p3)

        flip_play_attributes(p1)
        self.assertEqual(p1.history, p2.history)
        self.assertEqual(p1.cooperations, p2.cooperations)
        self.assertEqual(p1.defections, p2.defections)
        self.assertEqual(p1.state_distribution, p2.state_distribution)

    def test_dual_transformer_with_all_strategies(self):
        """Tests that DualTransformer produces the opposite results when faced
        with the same opponent history.
        """
        for s in axelrod.strategies:
            self.assert_dual_wrapper_correct(s)

    def test_dual_jossann_regression_test(self):
        player_class = JossAnnTransformer((0.2, 0.3))(axelrod.Alternator)
        self.assert_dual_wrapper_correct(player_class)

        player_class = JossAnnTransformer((0.5, 0.4))(axelrod.EvolvedLookerUp2_2_2)
        self.assert_dual_wrapper_correct(player_class)

    def test_dual_transformer_simple_play_regression_test(self):
        """DualTransformer has failed when there were multiple DualTransformers.
        It has also failed when DualTransformer was not the outermost
        transformer or when other transformers were between multiple
        DualTransformers."""
        multiple_dual_transformers = DualTransformer()(FlipTransformer()(DualTransformer()(axelrod.Cooperator)))()

        dual_transformer_not_first = IdentityTransformer()(DualTransformer()(axelrod.Cooperator))()

        for _ in range(3):
            multiple_dual_transformers.play(dual_transformer_not_first)

        self.assertEqual(multiple_dual_transformers.history, [D, D, D])
        self.assertEqual(dual_transformer_not_first.history, [D, D, D])

    def test_dual_transformer_multiple_interspersed_regression_test(self):
        """DualTransformer has failed when there were multiple DualTransformers.
        It has also failed when DualTransformer was not the outermost
        transformer or when other transformers were between multiple
        DualTransformers."""
        dual_not_first_transformer = IdentityTransformer()(DualTransformer()(axelrod.EvolvedANN))
        self.assert_dual_wrapper_correct(dual_not_first_transformer)

        multiple_dual_transformers = DualTransformer()(DualTransformer()(axelrod.WinStayLoseShift))
        self.assert_dual_wrapper_correct(multiple_dual_transformers)

    def assert_dual_wrapper_correct(self, player_class):
        turns = 100

        p1 = player_class()
        p2 = DualTransformer()(player_class)()
        p3 = axelrod.CyclerCCD()  # Cycles 'CCD'

        axelrod.seed(0)
        for _ in range(turns):
            p1.play(p3)

        p3.reset()

        axelrod.seed(0)
        for _ in range(turns):
            p2.play(p3)

        self.assertEqual(p1.history, [x.flip() for x in p2.history])

    def test_jossann_transformer(self):
        """Tests the JossAnn transformer.
        """
        probability = (1, 0)
        p1 = JossAnnTransformer(probability)(axelrod.Defector)()
        self.assertFalse(p1.classifier["stochastic"])
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, C, C, C])

        probability = (0, 1)
        p1 = JossAnnTransformer(probability)(axelrod.Cooperator)()
        self.assertFalse(p1.classifier["stochastic"])
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [D, D, D, D, D])

        probability = (0.3, 0.3)
        p1 = JossAnnTransformer(probability)(axelrod.TitForTat)()
        self.assertTrue(p1.classifier["stochastic"])

        p2 = axelrod.Cycler()
        axelrod.seed(0)
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [D, C, C, D, D])

        probability = (0.6, 0.6)
        p1 = JossAnnTransformer(probability)(axelrod.Cooperator)()
        self.assertTrue(p1.classifier["stochastic"])
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [D, C, D, D, C])

        probability = (0, 1)
        p1 = JossAnnTransformer(probability)(axelrod.Random)
        self.assertFalse(p1.classifier["stochastic"])
        self.assertFalse(p1().classifier["stochastic"])

        probability = (1, 0)
        p1 = JossAnnTransformer(probability)(axelrod.Random)
        self.assertFalse(p1.classifier["stochastic"])
        self.assertFalse(p1().classifier["stochastic"])

        probability = (.5, .5)
        p1 = JossAnnTransformer(probability)(axelrod.TitForTat)
        self.assertTrue(p1.classifier["stochastic"])
        self.assertTrue(p1().classifier["stochastic"])

        probability = (0, .5)
        p1 = JossAnnTransformer(probability)(axelrod.TitForTat)
        self.assertTrue(p1.classifier["stochastic"])
        self.assertTrue(p1().classifier["stochastic"])

        probability = (0, 0)
        p1 = JossAnnTransformer(probability)(axelrod.TitForTat)
        self.assertFalse(p1.classifier["stochastic"])
        self.assertFalse(p1().classifier["stochastic"])

        probability = (0, 0)
        p1 = JossAnnTransformer(probability)(axelrod.Random)
        self.assertTrue(p1.classifier["stochastic"])
        self.assertTrue(p1().classifier["stochastic"])


    def test_noisy_transformer(self):
        """Tests that the noisy transformed does flip some moves."""
        random.seed(5)
        # Cooperator to Defector
        p1 = axelrod.Cooperator()
        p2 = NoisyTransformer(0.5)(axelrod.Cooperator)()
        self.assertTrue(p2.classifier["stochastic"])
        for _ in range(10):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, C, C, C, D, D, C, C])

        p2 = NoisyTransformer(0)(axelrod.Cooperator)
        self.assertFalse(p2.classifier["stochastic"])
        self.assertFalse(p2().classifier["stochastic"])

        p2 = NoisyTransformer(1)(axelrod.Cooperator)
        self.assertFalse(p2.classifier["stochastic"])
        self.assertFalse(p2().classifier["stochastic"])

        p2 = NoisyTransformer(.3)(axelrod.Cooperator)
        self.assertTrue(p2.classifier["stochastic"])
        self.assertTrue(p2().classifier["stochastic"])

        p2 = NoisyTransformer(0)(axelrod.Random)
        self.assertTrue(p2.classifier["stochastic"])
        self.assertTrue(p2().classifier["stochastic"])

        p2 = NoisyTransformer(1)(axelrod.Random)
        self.assertTrue(p2.classifier["stochastic"])
        self.assertTrue(p2().classifier["stochastic"])


    def test_forgiving(self):
        """Tests that the forgiving transformer flips some defections."""
        random.seed(10)
        p1 = ForgiverTransformer(0.5)(axelrod.Alternator)()
        self.assertTrue(p1.classifier["stochastic"])
        p2 = axelrod.Defector()
        for _ in range(10):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, C, C, D, C, C, D, C, D])

        p1 = ForgiverTransformer(0)(axelrod.Alternator)()
        self.assertFalse(p1.classifier["stochastic"])

        p1 = ForgiverTransformer(1)(axelrod.Alternator)()
        self.assertFalse(p1.classifier["stochastic"])

    def test_initial_transformer(self):
        """Tests the InitialTransformer."""
        p1 = axelrod.Cooperator()
        self.assertEqual(p1.classifier["memory_depth"], 0)
        p2 = InitialTransformer([D, D])(axelrod.Cooperator)()
        self.assertEqual(p2.classifier["memory_depth"], 2)
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p2.history, [D, D, C, C, C])

        p1 = axelrod.Cooperator()
        p2 = InitialTransformer([D, D, C, D])(axelrod.Cooperator)()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p2.history, [D, D, C, D, C])

        p3 = InitialTransformer([D, D])(axelrod.Adaptive)()
        self.assertEqual(p3.classifier["memory_depth"], float('inf'))

    def test_final_transformer(self):
        """Tests the FinalTransformer when tournament length is known."""
        # Final play transformer
        p1 = axelrod.Cooperator()
        p2 = FinalTransformer([D, D, D])(axelrod.Cooperator)()
        self.assertEqual(p2.classifier['makes_use_of'], set(["length"]))
        self.assertEqual(p2.classifier['memory_depth'], 3)
        self.assertEqual(axelrod.Cooperator.classifier['makes_use_of'], set([]))

        p2.match_attributes["length"] = 6
        for _ in range(8):
            p1.play(p2)
        self.assertEqual(p2.history, [C, C, C, D, D, D, C, C])

        p3 = FinalTransformer([D, D])(axelrod.Adaptive)()
        self.assertEqual(p3.classifier["memory_depth"], float('inf'))

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
        self.assertFalse(MD.classifier["stochastic"])

        p1 = MD()
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, C, C, C])

        probability = 0
        MD = MixedTransformer(probability, axelrod.Cooperator)(axelrod.Defector)
        self.assertFalse(MD.classifier["stochastic"])

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
        self.assertTrue(MD.classifier["stochastic"])

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
        self.assertFalse(MD.classifier["stochastic"])

        p1 = MD()
        # Against a cooperator we see that we only defect
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
        p2 = DeadlockBreakingTransformer()(
            InitialTransformer([D])(axelrod.TitForTat))()
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

    def test_nice(self):
        """Tests the NiceTransformer."""
        p1 = NiceTransformer()(axelrod.Defector)()
        p2 = axelrod.Defector()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, D, D, D, D])
        self.assertEqual(p2.history, [D, D, D, D, D])

        p1 = NiceTransformer()(axelrod.Defector)()
        p2 = axelrod.Alternator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, D, D, D])
        self.assertEqual(p2.history, [C, D, C, D, C])

        p1 = NiceTransformer()(axelrod.Defector)()
        p2 = axelrod.Cooperator()
        for _ in range(5):
            p1.play(p2)
        self.assertEqual(p1.history, [C, C, C, C, C])
        self.assertEqual(p2.history, [C, C, C, C, C])

    def test_nilpotency(self):
        """Show that some of the transformers are (sometimes) nilpotent, i.e.
        that transformer(transformer(PlayerClass)) == PlayerClass"""
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
        transformer(transformer(PlayerClass)) == transformer(PlayerClass).
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


TFT = RetaliateUntilApologyTransformer()(axelrod.Cooperator)


class TestRUAisTFT(TestTitForTat):
    # This runs the 7 TFT tests when unittest is invoked
    player = TFT
    name = "RUA Cooperator"
    expected_classifier = {
        'memory_depth': 0,  # really 1
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
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
