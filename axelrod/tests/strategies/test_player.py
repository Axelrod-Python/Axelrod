import itertools
import pickle
import types
import unittest
import warnings

import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import integers, sampled_from

import axelrod as axl
from axelrod.tests.property import strategy_lists

C, D = axl.Action.C, axl.Action.D
random = axl.RandomGenerator()
short_run_time_short_mem = [
    s
    for s in axl.short_run_time_strategies
    if axl.Classifiers["memory_depth"](s()) <= 10
]


# Generic strategy functions for testing


def cooperate(*args):
    return C


def defect(*args):
    return D


# Test classifier used to create tests players
_test_classifier = {
    "memory_depth": 0,
    "stochastic": False,
    "makes_use_of": None,
    "inspects_source": False,
    "manipulates_source": False,
    "manipulates_state": False,
}


class ParameterisedTestPlayer(axl.Player):
    """A simple Player class for testing init parameters"""

    name = "ParameterisedTestPlayer"
    classifier = _test_classifier

    def __init__(self, arg_test1="testing1", arg_test2="testing2"):
        super().__init__()


class TestPlayerClass(unittest.TestCase):
    name = "Player"
    player = axl.Player
    classifier = {"stochastic": False}

    def test_seed_warning(self):
        """Test that the user is warned if a null seed is given."""
        player = self.player()
        with warnings.catch_warnings():
            player.set_seed(seed=None)

    def test_play(self):
        player1, player2 = self.player(), self.player()
        player1.strategy = cooperate
        player2.strategy = defect

        match = axl.Match((player1, player2), turns=1)
        match.play()

        self.assertEqual(player1.history[0], C)
        self.assertEqual(player2.history[0], D)
        # Test cooperation / defection counts
        self.assertEqual(player1.cooperations, 1)
        self.assertEqual(player1.defections, 0)
        self.assertEqual(player2.cooperations, 0)
        self.assertEqual(player2.defections, 1)
        # Test state distribution
        self.assertEqual(player1.state_distribution, {(C, D): 1})
        self.assertEqual(player2.state_distribution, {(D, C): 1})

        match = axl.Match((player1, player2), turns=2)
        match.play()
        self.assertEqual(player1.history[-1], C)
        self.assertEqual(player2.history[-1], D)
        # Test cooperation / defection counts
        self.assertEqual(player1.cooperations, 2)
        self.assertEqual(player1.defections, 0)
        self.assertEqual(player2.cooperations, 0)
        self.assertEqual(player2.defections, 2)
        # Test state distribution
        self.assertEqual(player1.state_distribution, {(C, D): 2})
        self.assertEqual(player2.state_distribution, {(D, C): 2})

    def test_state_distribution(self):
        player1 = axl.MockPlayer([C, C, D, D, C])
        player2 = axl.MockPlayer([C, D, C, D, D])
        match = axl.Match((player1, player2), turns=5)
        _ = match.play()
        self.assertEqual(
            player1.state_distribution,
            {(C, C): 1, (C, D): 2, (D, C): 1, (D, D): 1},
        )
        self.assertEqual(
            player2.state_distribution,
            {(C, C): 1, (C, D): 1, (D, C): 2, (D, D): 1},
        )

    def test_update_history(self):
        player = axl.Player()
        self.assertEqual(player.history, [])
        self.assertEqual(player.cooperations, 0)
        self.assertEqual(player.defections, 0)
        player.history.append(D, C)
        self.assertEqual(player.history, [D])
        self.assertEqual(player.defections, 1)
        self.assertEqual(player.cooperations, 0)
        player.history.append(C, C)
        self.assertEqual(player.history, [D, C])
        self.assertEqual(player.defections, 1)
        self.assertEqual(player.cooperations, 1)

    def test_history_assignment(self):
        player = axl.Player()
        with self.assertRaises(AttributeError):
            player.history = []

    def test_strategy(self):
        self.assertRaises(
            NotImplementedError, self.player().strategy, self.player()
        )

    def test_clone(self):
        """Tests player cloning."""
        player1 = axl.Random(p=0.75)  # 0.5 is the default
        player2 = player1.clone()
        turns = 50
        for op in [axl.Cooperator(), axl.Defector(), axl.TitForTat()]:
            seed = random.randint(0, 10**6)
            for p in [player1, player2]:
                m = axl.Match((p, op), turns=turns, reset=True, seed=seed)
                m.play()
            self.assertEqual(len(player1.history), turns)
            self.assertEqual(player1.history, player2.history)

    def test_equality(self):
        """Test the equality method for some bespoke cases"""
        # Check repr
        p1 = axl.Cooperator()
        p2 = axl.Cooperator()
        self.assertEqual(p1, p2)
        p1.__repr__ = lambda: "John Nash"
        self.assertNotEqual(p1, p2)

        # Check attributes
        p1 = axl.Cooperator()
        p2 = axl.Cooperator()
        p1.test = "29"
        self.assertNotEqual(p1, p2)

        p1 = axl.Cooperator()
        p2 = axl.Cooperator()
        p2.test = "29"
        self.assertNotEqual(p1, p2)

        p1.test = "29"
        self.assertEqual(p1, p2)

        # Check that attributes of both players are tested.
        p1.another_attribute = [1, 2, 3]
        self.assertNotEqual(p1, p2)
        p2.another_attribute = [1, 2, 3]
        self.assertEqual(p1, p2)

        p2.another_attribute_2 = {1: 2}
        self.assertNotEqual(p1, p2)
        p1.another_attribute_2 = {1: 2}
        self.assertEqual(p1, p2)

    def test_equality_for_numpy_array(self):
        """Check numpy array attribute (a special case)"""
        p1 = axl.Cooperator()
        p2 = axl.Cooperator()

        p1.array = np.array([0, 1])
        p2.array = np.array([0, 1])
        self.assertEqual(p1, p2)

        p2.array = np.array([1, 0])
        self.assertNotEqual(p1, p2)

    def test_equality_for_generator(self):
        """Test equality works with generator attribute and that the generator
        attribute is not altered during checking of equality"""
        p1 = axl.Cooperator()
        p2 = axl.Cooperator()

        # Check that players are equal with generator
        p1.generator = (i for i in range(10))
        p2.generator = (i for i in range(10))
        self.assertEqual(p1, p2)

        # Check state of one generator (ensure it hasn't changed)
        n = next(p2.generator)
        self.assertEqual(n, 0)

        # Players are no longer equal (one generator has changed)
        self.assertNotEqual(p1, p2)

        # Check that internal generator object has not been changed for either
        # player after latest equal check.
        self.assertEqual(list(p1.generator), list(range(10)))
        self.assertEqual(list(p2.generator), list(range(1, 10)))

        # Check that type is generator
        self.assertIsInstance(p2.generator, types.GeneratorType)

    def test_equality_for_cycle(self):
        """Test equality works with cycle attribute and that the cycle attribute
        is not altered during checking of equality"""
        # Check cycle attribute (a special case)
        p1 = axl.Cooperator()
        p2 = axl.Cooperator()

        # Check that players are equal with cycle
        p1.cycle = itertools.cycle(range(10))
        p2.cycle = itertools.cycle(range(10))
        self.assertEqual(p1, p2)

        # Check state of one generator (ensure it hasn't changed)
        n = next(p2.cycle)
        self.assertEqual(n, 0)

        # Players are no longer equal (one generator has changed)
        self.assertNotEqual(p1, p2)

        # Check that internal cycle object has not been changed for either
        # player after latest not equal check.
        self.assertEqual(next(p1.cycle), 0)
        self.assertEqual(next(p2.cycle), 1)

        # Check that type is cycle
        self.assertIsInstance(p2.cycle, itertools.cycle)

    def test_equality_on_init(self):
        """Test instances of all strategies are equal on init"""
        for s in axl.strategies:
            p1, p2 = s(), s()
            # Check three times (so testing equality doesn't change anything)
            self.assertEqual(p1, p2)
            self.assertEqual(p1, p2)
            self.assertEqual(p1, p2)

    def test_equality_with_player_as_attributes(self):
        """Test for a strange edge case where players have pointers to each
        other"""
        p1 = axl.Cooperator()
        p2 = axl.Cooperator()

        # If pointing at each other
        p1.player = p2
        p2.player = p1
        self.assertEqual(p1, p2)

        # Still checking other attributes.
        p1.test_attribute = "29"
        self.assertNotEqual(p1, p2)

        # If pointing at same strategy instances
        p1.player = axl.Cooperator()
        p2.player = axl.Cooperator()
        p2.test_attribute = "29"
        self.assertEqual(p1, p2)

        # If pointing at different strategy instances
        p1.player = axl.Cooperator()
        p2.player = axl.Defector()
        self.assertNotEqual(p1, p2)

        # If different strategies pointing at same strategy instances
        p3 = axl.Defector()
        p1.player = axl.Cooperator()
        p3.player = axl.Cooperator()
        self.assertNotEqual(p1, p3)

    def test_init_params(self):
        """Tests player correct parameters signature detection."""
        self.assertEqual(self.player.init_params(), {})
        self.assertEqual(
            ParameterisedTestPlayer.init_params(),
            {"arg_test1": "testing1", "arg_test2": "testing2"},
        )
        self.assertEqual(
            ParameterisedTestPlayer.init_params(arg_test1="other"),
            {"arg_test1": "other", "arg_test2": "testing2"},
        )
        self.assertEqual(
            ParameterisedTestPlayer.init_params(arg_test2="other"),
            {"arg_test1": "testing1", "arg_test2": "other"},
        )
        self.assertEqual(
            ParameterisedTestPlayer.init_params("other"),
            {"arg_test1": "other", "arg_test2": "testing2"},
        )

    def test_init_kwargs(self):
        """Tests player  correct parameters caching."""

        # Tests for Players with no init parameters

        # Test that init_kwargs exist and are empty
        self.assertEqual(self.player().init_kwargs, {})
        # Test that passing a positional argument raises an error
        self.assertRaises(TypeError, axl.Player, "test")
        # Test that passing a keyword argument raises an error
        self.assertRaises(TypeError, axl.Player, arg_test1="test")

        # Tests for Players with init parameters

        # Test that init_kwargs exist and contains default values
        self.assertEqual(
            ParameterisedTestPlayer().init_kwargs,
            {"arg_test1": "testing1", "arg_test2": "testing2"},
        )
        # Test that passing a keyword argument successfully change the
        # init_kwargs dict.
        self.assertEqual(
            ParameterisedTestPlayer(arg_test1="other").init_kwargs,
            {"arg_test1": "other", "arg_test2": "testing2"},
        )
        self.assertEqual(
            ParameterisedTestPlayer(arg_test2="other").init_kwargs,
            {"arg_test1": "testing1", "arg_test2": "other"},
        )
        # Test that passing a positional argument successfully change the
        # init_kwargs dict.
        self.assertEqual(
            ParameterisedTestPlayer("other", "other2").init_kwargs,
            {"arg_test1": "other", "arg_test2": "other2"},
        )
        # Test that passing an unknown keyword argument or a spare one raises
        # an error.
        self.assertRaises(TypeError, ParameterisedTestPlayer, arg_test3="test")
        self.assertRaises(
            TypeError, ParameterisedTestPlayer, "other", "other", "other"
        )


class TestOpponent(axl.Player):
    """A player who only exists so we have something to test against"""

    name = "TestOpponent"
    classifier = _test_classifier

    @staticmethod
    def strategy(opponent):
        return C


class TestPlayer(unittest.TestCase):
    """A Test class from which other player test classes are inherited."""

    player = TestOpponent
    expected_class_classifier = None

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        if self.__class__ != TestPlayer:
            player = self.player()
            self.assertEqual(len(player.history), 0)
            self.assertEqual(
                player.match_attributes,
                {"length": -1, "game": axl.DefaultGame, "noise": 0},
            )
            self.assertEqual(player.cooperations, 0)
            self.assertEqual(player.defections, 0)
            self.classifier_test(self.expected_class_classifier)

    def test_repr(self):
        """Test that the representation is correct."""
        if self.__class__ != TestPlayer:
            self.assertEqual(str(self.player()), self.name)

    def test_match_attributes(self):
        player = self.player()
        # Default
        player.set_match_attributes()
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs["length"], -1)
        self.assertEqual(t_attrs["noise"], 0)
        self.assertEqual(t_attrs["game"].RPST(), (3, 1, 0, 5))

        # Common
        player.set_match_attributes(length=200)
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs["length"], 200)
        self.assertEqual(t_attrs["noise"], 0)
        self.assertEqual(t_attrs["game"].RPST(), (3, 1, 0, 5))

        # Noisy
        player.set_match_attributes(length=200, noise=0.5)
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs["noise"], 0.5)

    def equality_of_players_test(self, p1, p2, seed, opponent):
        a1 = opponent()
        a2 = opponent()
        self.assertEqual(p1, p2)
        for player, op in [(p1, a1), (p2, a2)]:
            m = axl.Match(players=(player, op), turns=10, seed=seed)
            m.play()
        self.assertEqual(p1, p2)
        p1 = pickle.loads(pickle.dumps(p1))
        p2 = pickle.loads(pickle.dumps(p2))
        self.assertEqual(p1, p2)

    @given(
        opponent=sampled_from(short_run_time_short_mem),
        seed=integers(min_value=1, max_value=200),
    )
    @settings(
        max_examples=1,
        deadline=None,
        suppress_health_check=(HealthCheck.differing_executors,),
    )
    def test_equality_of_clone(self, seed, opponent):
        p1 = self.player()
        p2 = p1.clone()
        self.equality_of_players_test(p1, p2, seed, opponent)

    @given(
        opponent=sampled_from(axl.short_run_time_strategies),
        seed=integers(min_value=1, max_value=200),
    )
    @settings(
        max_examples=1,
        deadline=None,
        suppress_health_check=(HealthCheck.differing_executors,),
    )
    def test_equality_of_pickle_clone(self, seed, opponent):
        p1 = self.player()
        p2 = pickle.loads(pickle.dumps(p1))
        self.equality_of_players_test(p1, p2, seed, opponent)

    def test_reset_history_and_attributes(self):
        """Make sure resetting works correctly."""
        for opponent in [
            axl.Defector(),
            axl.Random(),
            axl.Alternator(),
            axl.Cooperator(),
        ]:
            player = self.player()
            clone = player.clone()
            match = axl.Match((player, opponent), turns=10, seed=111)
            match.play()
            player.reset()
            self.assertEqual(player, clone)

    def test_reset_clone(self):
        """Make sure history resetting with cloning works correctly, regardless
        if self.test_reset() is overwritten."""
        player = self.player()
        clone = player.clone()
        self.assertEqual(player, clone)

    @given(
        seed=integers(min_value=1, max_value=20000000),
        turns=integers(min_value=5, max_value=10),
        noise=integers(min_value=0, max_value=10),
    )
    @settings(
        max_examples=1,
        deadline=None,
        suppress_health_check=(HealthCheck.differing_executors,),
    )
    def test_clone_reproducible_play(self, seed, turns, noise):
        # Test that the cloned player produces identical play
        player = self.player()
        if player.name in ["Darwin", "Human"]:
            # Known exceptions
            return

        for op in [
            axl.Cooperator(),
            axl.Defector(),
            axl.TitForTat(),
            axl.Random(p=0.5),
        ]:
            player = self.player()
            player_clone = player.clone()
            op = op.clone()
            op_clone = op.clone()
            m1 = axl.Match(
                (player, op), turns=turns, seed=seed, noise=noise / 100.0
            )
            m2 = axl.Match(
                (player_clone, op_clone),
                turns=turns,
                seed=seed,
                noise=noise / 100.0,
            )
            m1.play()
            m2.play()
            self.assertEqual(m1.result, m2.result)
            self.assertEqual(player, player_clone)
            self.assertEqual(op, op_clone)

    @given(
        strategies=strategy_lists(
            max_size=5, strategies=short_run_time_short_mem
        ),
        seed=integers(min_value=1, max_value=200),
        turns=integers(min_value=1, max_value=200),
    )
    @settings(
        max_examples=1,
        deadline=None,
        suppress_health_check=(HealthCheck.differing_executors,),
    )
    def test_memory_depth_upper_bound(self, strategies, seed, turns):
        """
        Test that the memory depth is indeed an upper bound.
        """

        def get_memory_depth_or_zero(player):
            # Some of the test strategies have no entry in the classifiers
            # table, so there isn't logic to load default value of zero.
            memory = axl.Classifiers["memory_depth"](player)
            return memory if memory else 0

        player = self.player()
        memory = get_memory_depth_or_zero(player)
        if memory < float("inf"):
            for strategy in strategies:
                player.reset()
                opponent = strategy()
                max_memory = max(memory, get_memory_depth_or_zero(opponent))
                self.assertTrue(
                    test_memory(
                        player=player,
                        opponent=opponent,
                        seed=seed,
                        turns=turns,
                        memory_length=max_memory,
                    ),
                    msg="{} failed for seed={} and opponent={}".format(
                        player.name, seed, opponent
                    ),
                )

    def versus_test(
        self,
        opponent,
        expected_actions,
        turns=None,
        noise=None,
        seed=None,
        match_attributes=None,
        attrs=None,
        init_kwargs=None,
    ):
        """
        Tests a sequence of outcomes for two given players.
        Parameters:
        -----------
        opponent: Player or list
            An instance of a player OR a sequence of actions. If a sequence of
            actions is passed, a Mock Player is created that cycles over that
            sequence.
        expected_actions: List
            The expected outcomes of the match (list of tuples of actions).
        noise: float
            Any noise to be passed to a match
        seed: int
            The random seed to be used
        match_attributes: dict
            The match attributes to be passed to the players.  For example,
            `{length:-1}` implies that the players do not know the length of the
            match.
        attrs: dict
            Dictionary of internal attributes to check at the end of all plays
            in player
        init_kwargs: dict
            A dictionary of keyword arguments to instantiate player with
        """

        if init_kwargs is None:
            init_kwargs = dict()

        player = self.player(**init_kwargs)

        test_match = TestMatch()
        test_match.versus_test(
            player,
            opponent,
            [x for (x, y) in expected_actions],
            [y for (x, y) in expected_actions],
            turns=turns,
            noise=noise,
            seed=seed,
            attrs=attrs,
            match_attributes=match_attributes,
        )

    def classifier_test(self, expected_class_classifier=None):
        """Test that the keys in the expected_classifier dictionary give the
        expected values in the player classifier dictionary. Also checks that
        two particular keys (memory_depth and stochastic) are in the
        dictionary."""
        player = self.player()

        # Test that player has same classifier as its class unless otherwise
        # specified
        if expected_class_classifier is None:
            expected_class_classifier = player.classifier
        actual_class_classifier = {
            c: axl.Classifiers[c](player)
            for c in expected_class_classifier.keys()
        }
        self.assertEqual(expected_class_classifier, actual_class_classifier)

        self.assertTrue(
            "memory_depth" in player.classifier,
            msg="memory_depth not in classifier",
        )
        self.assertTrue(
            "stochastic" in player.classifier,
            msg="stochastic not in classifier",
        )
        for key in TestOpponent.classifier:
            self.assertEqual(
                axl.Classifiers[key](player),
                self.expected_classifier[key],
                msg="%s - Behaviour: %s != Expected Behaviour: %s"
                % (
                    key,
                    axl.Classifiers[key](player),
                    self.expected_classifier[key],
                ),
            )


class TestMatch(unittest.TestCase):
    """Test class for heads up play between two given players. Plays an
    axelrod match between the two players."""

    def versus_test(
        self,
        player1,
        player2,
        expected_actions1,
        expected_actions2,
        turns=None,
        noise=None,
        seed=None,
        match_attributes=None,
        attrs=None,
    ):
        """Tests a sequence of outcomes for two given players."""
        if len(expected_actions1) != len(expected_actions2):
            raise ValueError("Mismatched Expected History in TestMatch.")
        if not turns:
            turns = len(expected_actions1)

        match = axl.Match(
            (player1, player2),
            turns=turns,
            noise=noise,
            seed=seed,
            match_attributes=match_attributes,
        )
        match.play()

        # Test expected sequence of plays from the match is as expected.
        for i, (play, expected_play) in enumerate(
            zip(player1.history, expected_actions1)
        ):
            self.assertEqual((i, play), (i, expected_play))
        for i, (play, expected_play) in enumerate(
            zip(player2.history, expected_actions2)
        ):
            self.assertEqual((i, play), (i, expected_play))

        # Test final player attributes are as expected
        if attrs:
            for attr, value in attrs.items():
                self.assertEqual(getattr(player1, attr), value)

    def search_seeds(self, *args, **kwargs):  # pragma: no cover
        """Search for a seed that will pass the test. Use to find a new seed
        for a versus_test by changing self.versus_test to self.search_seeds
        within a TestPlayer or TestMatch class.
        """
        for seed in range(1, 100000):
            try:
                kwargs["seed"] = seed
                self.versus_test(*args, **kwargs)
            except AssertionError:
                continue
            else:
                print(seed)
                return seed
        return None

    def test_versus_with_incorrect_history_lengths(self):
        """Test the error raised by versus_test if expected actions do not
        match up."""
        with self.assertRaises(ValueError):
            p1, p2 = axl.Cooperator(), axl.Cooperator()
            actions1 = [C, C]
            actions2 = [C]
            self.versus_test(p1, p2, actions1, actions2)


@pytest.mark.skip(reason="This is a function used to test other strategies.")
def test_four_vector(test_class, expected_dictionary):
    """
    Checks that two dictionaries match -- the four-vector defining
    a memory-one strategy and the given expected dictionary.
    """
    player1 = test_class.player()
    for key in sorted(expected_dictionary.keys(), key=str):
        test_class.assertAlmostEqual(
            player1._four_vector[key], expected_dictionary[key]
        )


@pytest.mark.skip(reason="This is a function used to test other strategies.")
def test_memory(player, opponent, memory_length, seed=0, turns=10):
    """
    Checks if a player reacts to the plays of an opponent in the same way if
    only the given amount of memory is used.
    """
    # Play the match normally.
    match = axl.Match((player, opponent), turns=turns, seed=seed)
    plays = [p[0] for p in match.play()]

    # Play with limited history.
    player.reset()
    opponent.reset()
    player._history = axl.LimitedHistory(memory_length)
    opponent._history = axl.LimitedHistory(memory_length)
    match = axl.Match((player, opponent), turns=turns, reset=False, seed=seed)
    limited_plays = [p[0] for p in match.play()]

    return plays == limited_plays


class TestMemoryTest(unittest.TestCase):
    """
    Test for the memory test function.
    """

    def test_passes(self):
        """
        The memory test function returns True in this case as the correct mem
        length is used
        """
        player = axl.TitFor2Tats()
        opponent = axl.Defector()
        self.assertTrue(test_memory(player, opponent, memory_length=2))

    def test_failures(self):
        """
        The memory test function returns False in this case as the incorrect mem
        length is used
        """
        player = axl.TitFor2Tats()
        opponent = axl.Defector()
        self.assertFalse(test_memory(player, opponent, memory_length=1))
