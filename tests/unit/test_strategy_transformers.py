import axelrod as axl
from axelrod.strategy_transformers import *
from axelrod.tests.strategies.test_cooperator import TestCooperator
from axelrod.tests.strategies.test_defector import TestDefector
from axelrod.tests.strategies.test_player import TestMatch, TestPlayer
from axelrod.tests.strategies.test_titfortat import TestTitForTat

C, D = axl.Action.C, axl.Action.D


@FlipTransformer(name_prefix=None)
class CanPickle(axl.Cooperator):
    pass


@FlipTransformer()
class CanNotPickle(axl.Cooperator):
    pass


class TestTransformers(TestMatch):
    """Test generic transformer properties."""

    def test_player_can_be_pickled(self):
        player = axl.Cooperator()
        self.assertTrue(player_can_be_pickled(player))

        player = IdentityTransformer()(axl.Cooperator)()
        self.assertFalse(player_can_be_pickled(player))

        player = CanPickle()
        self.assertTrue(player_can_be_pickled(player))

        player = CanNotPickle()
        self.assertFalse(player_can_be_pickled(player))

    def test_is_strategy_static(self):
        self.assertTrue(is_strategy_static(axl.Cooperator))
        self.assertFalse(is_strategy_static(axl.Alternator))

    def test_is_strategy_static_with_inherited_strategy(self):
        class NewCooperator(axl.Cooperator):
            pass

        class NewAlternator(axl.Alternator):
            pass

        self.assertTrue(is_strategy_static(NewCooperator))
        self.assertFalse(is_strategy_static(NewAlternator))

    def test_DecoratorReBuilder(self):
        new_prefix = "YOLO"
        decorator = NoisyTransformer(0.2, name_prefix=new_prefix)

        factory_args = (noisy_wrapper, "Noisy", noisy_reclassifier)
        args = decorator.args
        kwargs = decorator.kwargs.copy()

        new_decorator = DecoratorReBuilder()(
            factory_args, args, kwargs, new_prefix
        )

        self.assertEqual(
            decorator(axl.Cooperator)(), new_decorator(axl.Cooperator)()
        )

    def test_StrategyReBuilder_declared_class_with_name_prefix(self):
        player = CanNotPickle()
        self.assertEqual(player.__class__.__name__, "FlippedCanNotPickle")

        decorators = [player.decorator]
        import_name = "CanNotPickle"
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

    def test_StrategyReBuilder_dynamically_wrapped_class_with_name_prefix(self):
        player = FlipTransformer()(axl.Cooperator)()
        self.assertEqual(player.__class__.__name__, "FlippedCooperator")

        decorators = [player.decorator]
        import_name = "Cooperator"
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

    def test_StrategyReBuilder_dynamically_wrapped_class_no_name_prefix(self):
        player = IdentityTransformer()(axl.Cooperator)()
        self.assertEqual(player.__class__.__name__, "Cooperator")

        decorators = [player.decorator]
        import_name = "Cooperator"
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

    def test_StrategyReBuilder_many_decorators(self):
        decorator_1 = IdentityTransformer()
        decorator_2 = FlipTransformer()
        decorator_3 = DualTransformer()
        player = decorator_3(decorator_2(decorator_1(axl.Cooperator)))()
        self.assertEqual(player.__class__.__name__, "DualFlippedCooperator")

        decorators = [decorator_1, decorator_2, decorator_3]
        import_name = "Cooperator"
        module_name = player.__module__

        new_player = StrategyReBuilder()(decorators, import_name, module_name)

        update_dict = player.__dict__.copy()

        new_player.__dict__.update(update_dict)
        self.assertEqual(player, new_player)

    def test_naming(self):
        """Tests that the player and class names are properly modified."""
        cls = FlipTransformer()(axl.Cooperator)
        p1 = cls()
        self.assertEqual(cls.__name__, "FlippedCooperator")
        self.assertEqual(p1.name, "Flipped Cooperator")

        cls = ForgiverTransformer(0.5)(axl.Alternator)
        p1 = cls()
        self.assertEqual(cls.__name__, "ForgivingAlternator")
        self.assertEqual(p1.name, "Forgiving Alternator")

        cls = ForgiverTransformer(0.5, name_prefix="")(axl.Alternator)
        p1 = cls()
        self.assertEqual(cls.__name__, "Alternator")
        self.assertEqual(p1.name, "Alternator")

    def test_repr(self):
        """Tests that the player __repr__ is properly modified to add
        Transformer's parameters.
        """
        self.assertEqual(
            str(ForgiverTransformer(0.5)(axl.Alternator)()),
            "Forgiving Alternator: 0.5",
        )
        self.assertEqual(
            str(InitialTransformer([D, D, C])(axl.Alternator)()),
            "Initial Alternator: [D, D, C]",
        )
        self.assertEqual(
            str(FlipTransformer()(axl.Random)(0.1)), "Flipped Random: 0.1"
        )
        self.assertEqual(
            str(
                MixedTransformer(0.3, (axl.Alternator, axl.Bully))(axl.Random)(
                    0.1
                )
            ),
            "Mutated Random: 0.1: 0.3, ['Alternator', 'Bully']",
        )

    def test_doc(self):
        """Test that the original docstring is present"""
        player = axl.Alternator()
        transformer = InitialTransformer([D, D, C])(axl.Alternator)()
        self.assertEqual(player.__doc__, transformer.__doc__)

    def test_cloning(self):
        """Tests that Player.clone preserves the application of transformations."""
        p1 = axl.Cooperator()
        p2 = FlipTransformer()(axl.Cooperator)()  # Defector
        p3 = p2.clone()
        match = axl.Match((p1, p3), turns=2)
        results = match.play()
        self.assertEqual(results, [(C, D), (C, D)])

    def test_composition(self):
        """Tests explicitly that transformations can be chained or composed."""
        cls1 = InitialTransformer([D, D])(axl.Cooperator)
        cls2 = FinalTransformer([D, D])(cls1)
        p1 = cls2()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D, D, C, C, C, C, D, D], [C] * 8)

        cls1 = FinalTransformer([D, D])(
            InitialTransformer([D, D])(axl.Cooperator)
        )
        p1 = cls1()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D, D, C, C, C, C, D, D], [C] * 8)

    def test_compose_transformers(self):
        """Tests explicitly that transformations can be chained or composed using
        compose_transformers."""
        cls1 = compose_transformers(
            FinalTransformer([D, D]), InitialTransformer([D, D])
        )
        p1 = cls1(axl.Cooperator)()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D, D, C, C, C, C, D, D], [C] * 8)

    def test_reclassification(self):
        """Tests that reclassifiers properly work."""

        def stochastic_reclassifier(original_classifier, *args):
            original_classifier["stochastic"] = True
            return original_classifier

        def deterministic_reclassifier(original_classifier, *args):
            original_classifier["stochastic"] = False
            return original_classifier

        StochasticTransformer = StrategyTransformerFactory(
            generic_strategy_wrapper, reclassifier=stochastic_reclassifier
        )
        DeterministicTransformer = StrategyTransformerFactory(
            generic_strategy_wrapper, reclassifier=deterministic_reclassifier
        )

        # Cooperator is not stochastic
        self.assertFalse(axl.Cooperator().classifier["stochastic"])
        # Transform makes it stochastic
        player = StochasticTransformer()(axl.Cooperator)()
        self.assertTrue(player.classifier["stochastic"])

        # Composing transforms should return it to not being stochastic
        cls1 = compose_transformers(
            DeterministicTransformer(), StochasticTransformer()
        )
        player = cls1(axl.Cooperator)()
        self.assertFalse(player.classifier["stochastic"])

        # Explicit composition
        player = DeterministicTransformer()(
            StochasticTransformer()(axl.Cooperator)
        )()
        self.assertFalse(player.classifier["stochastic"])

        # Random is stochastic
        self.assertTrue(axl.Random().classifier["stochastic"])

        # Transformer makes is not stochastic
        player = DeterministicTransformer()(axl.Random)()
        self.assertFalse(player.classifier["stochastic"])

        # Composing transforms should return it to being stochastic
        cls1 = compose_transformers(
            StochasticTransformer(), DeterministicTransformer()
        )
        player = cls1(axl.Random)()
        self.assertTrue(player.classifier["stochastic"])

        # Explicit composition
        player = StochasticTransformer()(
            DeterministicTransformer()(axl.Random)
        )()
        self.assertTrue(player.classifier["stochastic"])

    def test_nilpotency(self):
        """Show that some of the transformers are (sometimes) nilpotent, i.e.
        that transformer(transformer(PlayerClass)) == PlayerClass"""
        for transformer in [
            IdentityTransformer(),
            FlipTransformer(),
            TrackHistoryTransformer(),
        ]:
            for PlayerClass in [axl.Cooperator, axl.Defector]:
                for third_player in [axl.Cooperator(), axl.Defector()]:
                    player = PlayerClass()
                    transformed = transformer(transformer(PlayerClass))()
                    clone = third_player.clone()
                    match = axl.Match((player, third_player), turns=5)
                    match.play()
                    match = axl.Match((transformed, clone), turns=5)
                    match.play()
                    self.assertEqual(player.history, transformed.history)

    def test_idempotency(self):
        """Show that these transformers are idempotent, i.e. that
        transformer(transformer(PlayerClass)) == transformer(PlayerClass).
        That means that the transformer is a projection on the set of
        strategies."""
        for transformer in [
            IdentityTransformer(),
            GrudgeTransformer(1),
            FinalTransformer([C]),
            FinalTransformer([D]),
            InitialTransformer([C]),
            InitialTransformer([D]),
            DeadlockBreakingTransformer(),
            RetaliationTransformer(1),
            RetaliateUntilApologyTransformer(),
            TrackHistoryTransformer(),
            ApologyTransformer([D], [C]),
        ]:
            for PlayerClass in [axl.Cooperator, axl.Defector]:
                for third_player in [axl.Cooperator(), axl.Defector()]:
                    clone = third_player.clone()
                    player = transformer(PlayerClass)()
                    transformed = transformer(transformer(PlayerClass))()
                    match = axl.Match((player, third_player), turns=5)
                    match.play()
                    match = axl.Match((transformed, clone), turns=5)
                    match.play()
                    self.assertEqual(player.history, transformed.history)


class TestApologizingTransformer(TestMatch):
    def test_apology(self):
        """Tests the ApologyTransformer."""
        ApologizingDefector = ApologyTransformer([D], [C])(axl.Defector)
        p1 = ApologizingDefector()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D, C, D, C, D], [C] * 5)

    def test_apology2(self):
        ApologizingDefector = ApologyTransformer([D, D], [C, C])(axl.Defector)
        p1 = ApologizingDefector()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D, D, C, D, D, C], [C] * 6)


class TestDeadlockBreakingTransformer(TestMatch):
    def test_deadlock_breaks(self):
        """Test the DeadlockBreakingTransformer."""
        # We can induce a deadlock by altering TFT to defect first
        # No seed needed.
        self.versus_test(
            axl.TitForTat(),
            InitialTransformer([D])(axl.TitForTat)(),
            [C, D, C, D],
            [D, C, D, C],
        )

        # Now let's use the transformer to break the deadlock to achieve
        # Mutual cooperation
        # self.versus_test(
        self.versus_test(
            axl.TitForTat(),
            DeadlockBreakingTransformer()(
                InitialTransformer([D])(axl.TitForTat)
            )(),
            [C, D, C, C],
            [D, C, C, C],
        )


class TestDualTransformer(TestMatch):
    def assert_dual_wrapper_correct(self, player_class):
        """Show that against an identical opponent, the dual transformer
        reverses all actions correctly."""
        turns = 20
        seed = 1

        p1 = player_class()
        p2 = DualTransformer()(player_class)()
        p3 = axl.CyclerCCD()  # Cycles 'CCD'

        match = axl.Match((p1, p3), turns=turns, seed=seed)
        match.play()
        p3.reset()
        match = axl.Match((p2, p3), turns=turns, seed=seed)
        match.play()

        self.assertEqual(p1.history, [x.flip() for x in p2.history])

    def test_dual_transformer_with_all_strategies(self):
        """Tests that DualTransformer produces the opposite results when faced
        with the same opponent history.
        """
        for s in axl.short_run_time_strategies:
            self.assert_dual_wrapper_correct(s)

    def test_dual_jossann_regression_test(self):
        player_class = JossAnnTransformer((0.2, 0.3))(axl.Alternator)
        self.assert_dual_wrapper_correct(player_class)

        player_class = JossAnnTransformer((0.5, 0.4))(axl.EvolvedLookerUp2_2_2)
        self.assert_dual_wrapper_correct(player_class)

        player_class = JossAnnTransformer((0.2, 0.8))(axl.MetaHunter)
        self.assert_dual_wrapper_correct(player_class)

    def test_dual_transformer_simple_play_regression_test(self):
        """DualTransformer has failed when there were multiple DualTransformers.
        It has also failed when DualTransformer was not the outermost
        transformer or when other transformers were between multiple
        DualTransformers."""
        multiple_dual_transformers = DualTransformer()(
            FlipTransformer()(DualTransformer()(axl.Cooperator))
        )()

        dual_transformer_not_first = IdentityTransformer()(
            DualTransformer()(axl.Cooperator)
        )()

        self.versus_test(
            multiple_dual_transformers,
            dual_transformer_not_first,
            [D, D, D],
            [D, D, D],
        )

    def test_dual_transformer_multiple_interspersed_regression_test(self):
        """DualTransformer has failed when there were multiple DualTransformers.
        It has also failed when DualTransformer was not the outermost
        transformer or when other transformers were between multiple
        DualTransformers."""
        dual_not_first_transformer = IdentityTransformer()(
            DualTransformer()(axl.EvolvedANN)
        )
        self.assert_dual_wrapper_correct(dual_not_first_transformer)

        multiple_dual_transformers = DualTransformer()(
            DualTransformer()(axl.WinStayLoseShift)
        )
        self.assert_dual_wrapper_correct(multiple_dual_transformers)


class TestFinalTransformer(TestMatch):
    def test_final_transformer(self):
        """Tests the FinalTransformer when tournament length is known."""
        # Final play transformer
        p1 = axl.Cooperator()
        p2 = FinalTransformer([D, D, D])(axl.Cooperator)()
        self.assertEqual(axl.Classifiers["makes_use_of"](p2), {"length"})
        self.assertEqual(axl.Classifiers["memory_depth"](p2), 3)
        self.assertEqual(
            axl.Classifiers["makes_use_of"](axl.Cooperator()), set([])
        )
        self.versus_test(p1, p2, [C] * 8, [C, C, C, C, C, D, D, D], turns=8)

    def test_infinite_memory_depth_transformed(self):
        # Test on infinite memory depth, that memory depth isn't set to
        # a finite value
        p3 = FinalTransformer([D, D])(axl.Adaptive)()
        self.assertEqual(axl.Classifiers["memory_depth"](p3), float("inf"))

    def test_final_transformer_unknown_length(self):
        """Tests the FinalTransformer when tournament length is not known."""
        p1 = axl.Defector()
        p2 = FinalTransformer([D, D])(axl.Cooperator)()
        self.versus_test(
            p1, p2, [D] * 6, [C] * 6, match_attributes={"length": -1}
        )


class TestFlipTransformer(TestMatch):
    def test_flip_transformer(self):
        """Tests that FlipTransformer(Cooperator) == Defector."""
        p1 = axl.Cooperator()
        p2 = FlipTransformer()(axl.Cooperator)()  # Defector
        self.versus_test(p1, p2, [C] * 5, [D] * 5)

    def test_implementation(self):
        """A test that demonstrates the difference in outcomes if
        FlipTransformer is applied to Alternator and CyclerCD. In other words,
        the implementation matters, not just the outcomes."""
        p1 = axl.Cycler(cycle="CD")
        p2 = FlipTransformer()(axl.Cycler)(cycle="CD")
        self.versus_test(p1, p2, [C, D, C, D, C], [D, C, D, C, D])

        p1 = axl.Alternator()
        p2 = FlipTransformer()(axl.Alternator)()
        self.versus_test(p1, p2, [C, D, C, D, C], [D, D, D, D, D])


class TestForgivingTransformer(TestMatch):
    def test_forgiving_transformer(self):
        """Tests that the forgiving transformer flips some defections."""
        p1 = ForgiverTransformer(0.5)(axl.Alternator)()
        p2 = axl.Defector()
        turns = 10
        self.versus_test(
            p1, p2, [C, D, C, C, D, C, C, D, C, D], [D] * turns, seed=8
        )

    def test_stochastic_values_classifier(self):
        p1 = ForgiverTransformer(0.5)(axl.Alternator)()
        self.assertTrue(axl.Classifiers["stochastic"](p1))

    def test_deterministic_values_classifier(self):
        p1 = ForgiverTransformer(0)(axl.Alternator)()
        self.assertFalse(axl.Classifiers["stochastic"](p1))

        p1 = ForgiverTransformer(1)(axl.Alternator)()
        self.assertFalse(axl.Classifiers["stochastic"](p1))


class TestGrudgingTransformer(TestMatch):
    def test_grudging1(self):
        p1 = axl.Defector()
        p2 = GrudgeTransformer(1)(axl.Cooperator)()
        self.versus_test(p1, p2, [D, D, D, D], [C, C, D, D], seed=11)

    def test_grudging2(self):
        p1 = InitialTransformer([C])(axl.Defector)()
        p2 = GrudgeTransformer(2)(axl.Cooperator)()
        self.versus_test(
            p1, p2, [C, D, D, D, D, D, D, D], [C, C, C, C, D, D, D, D], seed=11
        )


class TestHistoryTrackingTransformer(TestMatch):
    def test_history_track(self):
        """Tests the tracked history matches."""
        p1 = axl.Cooperator()
        p2 = TrackHistoryTransformer()(axl.Random)()
        match = axl.Match((p1, p2), turns=6, seed=1)
        match.play()
        self.assertEqual(p2.history, p2._recorded_history)

    def test_actions_unaffected(self):
        """Tests that the history tracking transformer doesn't alter the play at all."""
        p1 = axl.Cooperator()
        p2 = TrackHistoryTransformer()(axl.Alternator)()
        self.versus_test(p1, p2, [C] * 8, [C, D] * 4)


class TestIdentityTransformer(TestMatch):
    def test_all_strategies(self):
        # Attempt to transform each strategy to ensure that implementation
        # choices (like use of super) do not cause issues
        for s in axl.strategies:
            opponent = axl.Cooperator()
            player = IdentityTransformer()(s)()
            match = axl.Match((player, opponent), turns=3)
            match.play()

    def test_generic(self):
        """Test that the generic wrapper does nothing."""
        # This is the identity transformer
        transformer = StrategyTransformerFactory(generic_strategy_wrapper)()
        Cooperator2 = transformer(axl.Cooperator)
        Defector2 = transformer(axl.Defector)

        turns = 100
        self.versus_test(
            axl.Cooperator(), Cooperator2(), [C] * turns, [C] * turns
        )
        self.versus_test(
            axl.Cooperator(), Defector2(), [C] * turns, [D] * turns
        )


class TestInitialTransformer(TestMatch):
    def test_initial_transformer(self):
        """Tests the InitialTransformer."""
        p1 = axl.Cooperator()
        self.assertEqual(axl.Classifiers["memory_depth"](p1), 0)
        p2 = InitialTransformer([D, D])(axl.Cooperator)()
        self.assertEqual(axl.Classifiers["memory_depth"](p2), 2)
        match = axl.Match((p1, p2), turns=5, seed=0)
        match.play()
        self.assertEqual(p2.history, [D, D, C, C, C])

        p1 = axl.Cooperator()
        p2 = InitialTransformer([D, D, C, D])(axl.Cooperator)()
        match = axl.Match((p1, p2), turns=5, seed=0)
        match.play()
        self.assertEqual(p2.history, [D, D, C, D, C])

        p3 = InitialTransformer([D, D])(axl.Adaptive)()
        self.assertEqual(axl.Classifiers["memory_depth"](p3), float("inf"))


class TestJossAnnTransformer(TestMatch):
    def test_deterministic_match(self):
        """Tests the JossAnn transformer."""
        probability = (1, 0)
        p1 = JossAnnTransformer(probability)(axl.Defector)()
        self.assertFalse(axl.Classifiers["stochastic"](p1))
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [C] * 5, [C] * 5)

        probability = (0, 1)
        p1 = JossAnnTransformer(probability)(axl.Cooperator)()
        self.assertFalse(axl.Classifiers["stochastic"](p1))
        self.versus_test(p1, p2, [D] * 5, [C] * 5)

    def test_meta_strategy(self):
        """Tests the JossAnn transformer on a Meta strategy to check
        for a regression."""
        probability = (1, 0)
        for player_class in [axl.MetaHunter, axl.MemoryDecay, axl.MetaWinner]:
            p1 = JossAnnTransformer(probability)(player_class)()
            self.assertFalse(axl.Classifiers["stochastic"](p1))
            p2 = axl.Cooperator()
            m = axl.Match((p1, p2), turns=10)
            m.play()

    def test_deterministic_match_override(self):
        """Tests the JossAnn transformer."""
        probability = (1, 0)
        p1 = JossAnnTransformer(probability)(axl.Random)()
        self.assertFalse(axl.Classifiers["stochastic"](p1))
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [C] * 5, [C] * 5)

        probability = (0, 1)
        p1 = JossAnnTransformer(probability)(axl.Random)()
        self.assertFalse(axl.Classifiers["stochastic"](p1))
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D] * 5, [C] * 5)

    def test_stochastic1(self):
        probability = (0.3, 0.3)
        p1 = JossAnnTransformer(probability)(axl.TitForTat)()
        self.assertTrue(axl.Classifiers["stochastic"](p1))
        p2 = axl.Cycler()
        self.versus_test(p1, p2, [D, C, C, D, D], [C, C, D, C, C], seed=18)

    def test_stochastic2(self):
        probability = (0.6, 0.6)
        p1 = JossAnnTransformer(probability)(axl.Cooperator)()
        self.assertTrue(axl.Classifiers["stochastic"](p1))
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D, C, D, D, C], [C] * 5, seed=27)

    def test_stochastic_classifiers(self):
        probability = (0, 1)
        p1 = JossAnnTransformer(probability)(axl.Random)
        self.assertFalse(axl.Classifiers["stochastic"](p1()))

        probability = (1, 0)
        p1 = JossAnnTransformer(probability)(axl.Random)
        self.assertFalse(axl.Classifiers["stochastic"](p1()))

        probability = (0.5, 0.5)
        p1 = JossAnnTransformer(probability)(axl.TitForTat)
        self.assertTrue(axl.Classifiers["stochastic"](p1()))

        probability = (0, 0.5)
        p1 = JossAnnTransformer(probability)(axl.TitForTat)
        self.assertTrue(axl.Classifiers["stochastic"](p1()))

        probability = (0, 0)
        p1 = JossAnnTransformer(probability)(axl.TitForTat)
        self.assertTrue(axl.Classifiers["stochastic"](p1()))

        probability = (0, 0)
        p1 = JossAnnTransformer(probability)(axl.Random)
        self.assertTrue(axl.Classifiers["stochastic"](p1()))


class TestMixedTransformer(TestMatch):
    def test_mixed_transformer_deterministic(self):
        """Test changes in stochasticity."""
        probability = 1
        MD = MixedTransformer(probability, axl.Cooperator)(axl.Defector)
        self.assertFalse(axl.Classifiers["stochastic"](MD()))

        p1 = MD()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [C] * 5, [C] * 5)

        probability = 0
        MD = MixedTransformer(probability, axl.Cooperator)(axl.Defector)
        self.assertFalse(axl.Classifiers["stochastic"](MD()))

        p1 = MD()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D] * 5, [C] * 5)

    def test_mixed_transformer(self):
        # Decorating with list and distribution
        # Decorate a cooperator putting all weight on other strategies that are
        # 'nice'
        probability = [0.3, 0.2, 0]
        strategies = [axl.TitForTat, axl.Grudger, axl.Defector]
        MD = MixedTransformer(probability, strategies)(axl.Cooperator)
        self.assertTrue(axl.Classifiers["stochastic"](MD()))

        p1 = MD()
        # Against a cooperator we see that we only cooperate
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [C] * 5, [C] * 5)

        # Decorate a cooperator putting all weight on Defector
        probability = (0, 0, 1)  # Note can also pass tuple
        strategies = [axl.TitForTat, axl.Grudger, axl.Defector]
        MD = MixedTransformer(probability, strategies)(axl.Cooperator)
        self.assertFalse(axl.Classifiers["stochastic"](MD()))

        p1 = MD()
        # Against a cooperator we see that we only defect
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [D] * 5, [C] * 5)


class TestNiceTransformer(TestMatch):
    def test_nice1(self):
        """Tests the NiceTransformer."""
        p1 = NiceTransformer()(axl.Defector)()
        p2 = axl.Defector()
        self.versus_test(p1, p2, [C, D, D, D, D], [D, D, D, D, D])

    def test_nice2(self):
        p1 = NiceTransformer()(axl.Defector)()
        p2 = axl.Alternator()
        self.versus_test(p1, p2, [C, C, D, D, D], [C, D, C, D, C])

    def test_nice3(self):
        p1 = NiceTransformer()(axl.Defector)()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [C, C, C, C, C], [C, C, C, C, C])


class TestNoisyTransformer(TestMatch):
    def test_noisy_transformer(self):
        """Tests that the noisy transformed does flip some moves."""
        # Cooperator to Defector
        p1 = axl.Cooperator()
        p2 = NoisyTransformer(0.5)(axl.Cooperator)()
        self.assertTrue(axl.Classifiers["stochastic"](p2))
        self.versus_test(
            p1, p2, [C] * 10, [D, C, C, D, C, D, C, D, D, C], seed=1
        )

    def test_noisy_transformation_stochastic(self):
        """Depending on the value of the noise parameter, the strategy may become stochastic
        or deterministic."""
        # Deterministic --> Deterministic
        p2 = NoisyTransformer(1)(axl.Cooperator)
        self.assertFalse(axl.Classifiers["stochastic"](p2()))

        # Deterministic --> Stochastic
        p2 = NoisyTransformer(0.3)(axl.Cooperator)
        self.assertTrue(axl.Classifiers["stochastic"](p2()))

        # Stochastic --> Deterministic, case 0
        p2 = NoisyTransformer(0)(axl.Random)
        self.assertTrue(axl.Classifiers["stochastic"](p2()))

        # Stochastic --> Deterministic, case 1
        p2 = NoisyTransformer(1)(axl.Random)
        self.assertTrue(axl.Classifiers["stochastic"](p2()))


class TestRetailiateTransformer(TestMatch):
    def test_retailiating_cooperator_against_defector(self):
        """Tests the RetaliateTransformer."""
        p1 = RetaliationTransformer(1)(axl.Cooperator)()
        p2 = axl.Defector()
        self.versus_test(p1, p2, [C, D, D, D, D], [D, D, D, D, D])

    def test_retailiating_cooperator_against_alternator(self):
        p1 = RetaliationTransformer(1)(axl.Cooperator)()
        p2 = axl.Alternator()
        self.versus_test(p1, p2, [C, C, D, C, D], [C, D, C, D, C])

    def test_retailiating_cooperator_against_2TFT(self):
        TwoTitsForTat = RetaliationTransformer(2)(axl.Cooperator)
        p1 = TwoTitsForTat()
        p2 = axl.CyclerCCD()
        self.versus_test(
            p1, p2, [C, C, C, D, D, C, D, D, C], [C, C, D, C, C, D, C, C, D]
        )


class TestRetailiateUntilApologyTransformer(TestMatch):
    def test_retaliation_until_apology(self):
        """Tests the RetaliateUntilApologyTransformer."""
        TFT = RetaliateUntilApologyTransformer()(axl.Cooperator)
        p1 = TFT()
        p2 = axl.Cooperator()
        self.versus_test(p1, p2, [C, C], [C, C])

        p1 = TFT()
        p2 = axl.Defector()
        self.versus_test(p1, p2, [C, D], [D, D])

    def test_retaliation_until_apology_stochastic(self):
        TFT = RetaliateUntilApologyTransformer()(axl.Cooperator)
        p1 = TFT()
        p2 = axl.Random()
        self.versus_test(p1, p2, [C, C, D, D, C], [C, D, D, C, D], seed=1)


# Run the standard Player tests on some specifically transformed players


class TestNullInitialTransformedCooperator(TestPlayer):
    player = InitialTransformer([])(axl.Cooperator)
    name = "Initial Cooperator: []"
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestInitialTransformedCooperator(TestPlayer):
    player = InitialTransformer([D, D])(axl.Cooperator)
    name = "Initial Cooperator: [D, D]"
    expected_classifier = {
        "memory_depth": 2,
        "stochastic": False,
        "makes_use_of": set(),
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestFinalTransformedCooperator(TestPlayer):
    player = FinalTransformer([D, D, D])(axl.Cooperator)
    name = "Final Cooperator: [D, D, D]"
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": {"length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestInitialFinalTransformedCooperator(TestPlayer):
    player = InitialTransformer([D, D])(
        FinalTransformer([D, D, D])(axl.Cooperator)
    )
    name = "Initial Final Cooperator: [D, D, D]: [D, D]"
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": {"length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestFinalInitialTransformedCooperator(TestPlayer):
    player = FinalTransformer([D, D])(
        InitialTransformer([D, D, D])(axl.Cooperator)
    )
    name = "Final Initial Cooperator: [D, D, D]: [D, D]"
    expected_classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": {"length"},
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestRUACooperatorisTFT(TestTitForTat):
    player = RetaliateUntilApologyTransformer()(axl.Cooperator)
    name = "RUA Cooperator"
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestFlipDefector(TestCooperator):
    # Test that FlipTransformer(Defector) == Cooperator
    name = "Flipped Defector"
    player = FlipTransformer()(axl.Defector)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestNoisyNullCooperator(TestCooperator):
    name = "Noisy Cooperator: 0"
    player = NoisyTransformer(0)(axl.Cooperator)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestFullNoisyCooperatorIsDefector(TestDefector):
    name = "Noisy Cooperator: 1"
    player = NoisyTransformer(1)(axl.Cooperator)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestNullForgivingCooperator(TestDefector):
    name = "Forgiving Defector: 0"
    player = ForgiverTransformer(0)(axl.Defector)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestFullForgivingCooperatorIsDefector(TestCooperator):
    name = "Forgiving Defector: 1"
    player = ForgiverTransformer(1)(axl.Defector)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMixed0(TestDefector):
    name = "Mutated Defector: 0, <class 'axelrod.strategies.cooperator.Cooperator'>"
    player = MixedTransformer(0, axl.Cooperator)(axl.Defector)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestMixed1(TestDefector):
    name = (
        "Mutated Cooperator: 1, <class 'axelrod.strategies.defector.Defector'>"
    )
    player = MixedTransformer(1, axl.Defector)(axl.Cooperator)
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestIdentityDualTransformer(TestPlayer):
    name = "Dual Cooperator"
    player = IdentityTransformer()(DualTransformer()(axl.Cooperator))
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestFlippedDualTransformer(TestPlayer):
    name = "Flipped Dual Cooperator"
    player = FlipTransformer()(DualTransformer()(axl.Cooperator))
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestDualJossAnn(TestPlayer):
    name = "Dual Joss-Ann Alternator: (0.2, 0.3)"
    player = DualTransformer()(JossAnnTransformer((0.2, 0.3))(axl.Alternator))
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestJossAnnDual(TestPlayer):
    name = "Joss-Ann Dual Alternator: (0.2, 0.3)"
    player = JossAnnTransformer((0.2, 0.3))(DualTransformer()(axl.Alternator))
    expected_classifier = {
        "memory_depth": 1,
        "stochastic": True,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }


class TestJossAnnOverwriteClassifier(TestPlayer):
    name = "Joss-Ann Final Random: 0.5: [D, D]: (1.0, 0.0)"
    player = JossAnnTransformer((1.0, 0.0))(
        FinalTransformer([D, D])(axl.Random)
    )
    expected_classifier = {
        "memory_depth": 0,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }
