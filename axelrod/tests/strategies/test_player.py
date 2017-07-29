import random
import unittest
import types
import itertools
import numpy as np

import axelrod
from axelrod import DefaultGame, Player
from axelrod.player import get_state_distribution_from_history, update_history


C, D = axelrod.Action.C, axelrod.Action.D


# Generic strategy functions for testing

def cooperate(*args):
    return C


def defect(*args):
    return D

# Test classifier used to create tests players
_test_classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': None,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
}


class ParameterisedTestPlayer(Player):
    """A simple Player class for testing init parameters"""

    name = 'ParameterisedTestPlayer'
    classifier = _test_classifier

    def __init__(self, arg_test1='testing1', arg_test2='testing2'):
        super().__init__()


class TestPlayerClass(unittest.TestCase):

    name = "Player"
    player = Player
    classifier = {'stochastic': False}

    def test_add_noise(self):
        axelrod.seed(1)
        noise = 0.2
        s1, s2 = C, C
        noisy_s1, noisy_s2 = self.player()._add_noise(noise, s1, s2)
        self.assertEqual(noisy_s1, D)
        self.assertEqual(noisy_s2, C)

        noise = 0.9
        noisy_s1, noisy_s2 = self.player()._add_noise(noise, s1, s2)
        self.assertEqual(noisy_s1, D)
        self.assertEqual(noisy_s2, D)

    def test_play(self):
        player1, player2 = self.player(), self.player()
        player1.strategy = cooperate
        player2.strategy = defect
        player1.play(player2)
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

        player1.play(player2)
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
        player1 = axelrod.MockPlayer([C, C, D, D, C])
        player2 = axelrod.MockPlayer([C, D, C, D, D])
        match = axelrod.Match((player1, player2), turns=5)
        _ = match.play()
        self.assertEqual(player1.state_distribution,
                         {(C, C): 1, (C, D): 2, (D, C): 1, (D, D): 1})
        self.assertEqual(player2.state_distribution,
                         {(C, C): 1, (C, D): 1, (D, C): 2, (D, D): 1})

    def test_get_state_distribution_from_history(self):
        player = self.player()
        history_1 = [C, C, D, D, C]
        history_2 = [C, D, C, D, D]
        get_state_distribution_from_history(
            player, history_1, history_2)
        self.assertEqual(
            player.state_distribution,
            {(C, C): 1, (C, D): 2, (D, C): 1, (D, D): 1}
        )

    def test_noisy_play(self):
        axelrod.seed(1)
        noise = 0.2
        player1, player2 = self.player(), self.player()
        player1.strategy = cooperate
        player2.strategy = defect
        player1.play(player2, noise)
        self.assertEqual(player1.history[0], D)
        self.assertEqual(player2.history[0], D)

    def test_update_history(self):
        player = Player()
        self.assertEqual(player.history, [])
        self.assertEqual(player.cooperations, 0)
        self.assertEqual(player.defections, 0)
        update_history(player, D)
        self.assertEqual(player.history, [D])
        self.assertEqual(player.defections, 1)
        self.assertEqual(player.cooperations, 0)
        update_history(player, C)
        self.assertEqual(player.history, [D, C])
        self.assertEqual(player.defections, 1)
        self.assertEqual(player.cooperations, 1)

    def test_strategy(self):
        self.assertRaises(
            NotImplementedError, self.player().strategy, self.player())

    def test_clone(self):
        """Tests player cloning."""
        player1 = axelrod.Random(p=0.75)  # 0.5 is the default
        player2 = player1.clone()
        turns = 50
        for op in [axelrod.Cooperator(), axelrod.Defector(),
                   axelrod.TitForTat()]:
            player1.reset()
            player2.reset()
            seed = random.randint(0, 10 ** 6)
            for p in [player1, player2]:
                axelrod.seed(seed)
                m = axelrod.Match((p, op), turns=turns)
                m.play()
            self.assertEqual(len(player1.history), turns)
            self.assertEqual(player1.history, player2.history)

    def test_equality(self):
        """Test the equality method for some bespoke cases"""
        # Check repr
        p1 = axelrod.Cooperator()
        p2 = axelrod.Cooperator()
        self.assertEqual(p1, p2)
        p1.__repr__ = lambda: "John Nash"
        self.assertNotEqual(p1, p2)

        # Check attributes
        p1 = axelrod.Cooperator()
        p2 = axelrod.Cooperator()
        p1.test = "29"
        self.assertNotEqual(p1, p2)

        p1 = axelrod.Cooperator()
        p2 = axelrod.Cooperator()
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
        p1 = axelrod.Cooperator()
        p2 = axelrod.Cooperator()

        p1.array = np.array([0, 1])
        p2.array = np.array([0, 1])
        self.assertEqual(p1, p2)

        p2.array = np.array([1, 0])
        self.assertNotEqual(p1, p2)

    def test_equality_for_generator(self):
        """Test equality works with generator attribute and that the generator
        attribute is not altered during checking of equality"""
        p1 = axelrod.Cooperator()
        p2 = axelrod.Cooperator()

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
        p1 = axelrod.Cooperator()
        p2 = axelrod.Cooperator()

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
        for s in axelrod.strategies:
            p1, p2 = s(), s()
            # Check three times (so testing equality doesn't change anything)
            self.assertEqual(p1, p2)
            self.assertEqual(p1, p2)
            self.assertEqual(p1, p2)

    def test_equality_with_player_as_attributes(self):
        """Test for a strange edge case where players have pointers to each
        other"""
        p1 = axelrod.Cooperator()
        p2 = axelrod.Cooperator()

        # If pointing at each other
        p1.player = p2
        p2.player = p1
        self.assertEqual(p1, p2)

        # Still checking other attributes.
        p1.test_attribute = "29"
        self.assertNotEqual(p1, p2)

        # If pointing at same strategy instances
        p1.player = axelrod.Cooperator()
        p2.player = axelrod.Cooperator()
        p2.test_attribute = "29"
        self.assertEqual(p1, p2)

        # If pointing at different strategy instances
        p1.player = axelrod.Cooperator()
        p2.player = axelrod.Defector()
        self.assertNotEqual(p1, p2)

        # If different strategies pointing at same strategy instances
        p3 = axelrod.Defector()
        p1.player = axelrod.Cooperator()
        p3.player = axelrod.Cooperator()
        self.assertNotEqual(p1, p3)

    def test_init_params(self):
        """Tests player correct parameters signature detection."""
        self.assertEqual(self.player.init_params(), {})
        self.assertEqual(ParameterisedTestPlayer.init_params(),
                         {'arg_test1': 'testing1', 'arg_test2': 'testing2'})
        self.assertEqual(ParameterisedTestPlayer.init_params(arg_test1='other'),
                         {'arg_test1': 'other', 'arg_test2': 'testing2'})
        self.assertEqual(ParameterisedTestPlayer.init_params(arg_test2='other'),
                         {'arg_test1': 'testing1', 'arg_test2': 'other'})
        self.assertEqual(ParameterisedTestPlayer.init_params('other'),
                         {'arg_test1': 'other', 'arg_test2': 'testing2'})

    def test_init_kwargs(self):
        """Tests player  correct parameters caching."""

        # Tests for Players with no init parameters

        # Test that init_kwargs exist and are empty
        self.assertEqual(self.player().init_kwargs, {})
        # Test that passing a positional argument raises an error
        self.assertRaises(TypeError, Player, 'test')
        # Test that passing a keyword argument raises an error
        self.assertRaises(TypeError, Player, arg_test1='test')

        # Tests for Players with init parameters

        # Test that init_kwargs exist and contains default values
        self.assertEqual(ParameterisedTestPlayer().init_kwargs,
                         {'arg_test1': 'testing1', 'arg_test2': 'testing2'})
        # Test that passing a keyword argument successfully change the
        # init_kwargs dict.
        self.assertEqual(ParameterisedTestPlayer(arg_test1='other').init_kwargs,
                         {'arg_test1': 'other', 'arg_test2': 'testing2'})
        self.assertEqual(ParameterisedTestPlayer(arg_test2='other').init_kwargs,
                         {'arg_test1': 'testing1', 'arg_test2': 'other'})
        # Test that passing a positional argument successfully change the
        # init_kwargs dict.
        self.assertEqual(ParameterisedTestPlayer('other', 'other2').init_kwargs,
                         {'arg_test1': 'other', 'arg_test2': 'other2'})
        # Test that passing an unknown keyword argument or a spare one raises
        # an error.
        self.assertRaises(TypeError, ParameterisedTestPlayer, arg_test3='test')
        self.assertRaises(TypeError, ParameterisedTestPlayer, 'other', 'other',
                          'other')


class TestOpponent(Player):
    """A player who only exists so we have something to test against"""

    name = 'TestPlayer'
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
                {'length': -1, 'game': DefaultGame, 'noise': 0})
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
        self.assertEqual(t_attrs['length'], -1)
        self.assertEqual(t_attrs['noise'], 0)
        self.assertEqual(t_attrs['game'].RPST(), (3, 1, 0, 5))

        # Common
        player.set_match_attributes(length=200)
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs['length'], 200)
        self.assertEqual(t_attrs['noise'], 0)
        self.assertEqual(t_attrs['game'].RPST(), (3, 1, 0, 5))

        # Noisy
        player.set_match_attributes(length=200, noise=.5)
        t_attrs = player.match_attributes
        self.assertEqual(t_attrs['noise'], .5)

    def test_reset_history_and_attributes(self):
        """Make sure resetting works correctly."""
        player = self.player()
        clone = player.clone()
        for opponent in [axelrod.Defector(), axelrod.Random(),
                         axelrod.Alternator(), axelrod.Cooperator()]:

            for seed in range(10):
                axelrod.seed(seed)
                player.play(opponent)

            player.reset()
            self.assertEqual(player, clone)

    def test_reset_clone(self):
        """Make sure history resetting with cloning works correctly, regardless
        if self.test_reset() is overwritten."""
        player = self.player()
        clone = player.clone()
        self.assertEqual(player, clone)

    def test_clone(self):
        # Test that the cloned player produces identical play
        player1 = self.player()
        if player1.name in ["Darwin", "Human"]:
            # Known exceptions
            return
        player2 = player1.clone()
        self.assertEqual(len(player2.history), 0)
        self.assertEqual(player2.cooperations, 0)
        self.assertEqual(player2.defections, 0)
        self.assertEqual(player2.state_distribution, {})
        self.assertEqual(player2.classifier, player1.classifier)
        self.assertEqual(player2.match_attributes, player1.match_attributes)

        turns = 50
        r = random.random()
        for op in [axelrod.Cooperator(), axelrod.Defector(),
                   axelrod.TitForTat(), axelrod.Random(p=r)]:
            player1.reset()
            player2.reset()
            seed = random.randint(0, 10 ** 6)
            for p in [player1, player2]:
                axelrod.seed(seed)
                m = axelrod.Match((p, op), turns=turns)
                m.play()
            self.assertEqual(len(player1.history), turns)
            self.assertEqual(player1.history, player2.history)

    def versus_test(self, opponent, expected_actions,
                    noise=None, seed=None, turns=10,
                    match_attributes=None, attrs=None,
                    init_kwargs=None):
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
        length: int
            The length of the game. If `opponent` is a sequence of actions then
            the length is taken to be the length of the sequence.
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

        turns = len(expected_actions)
        if init_kwargs is None:
            init_kwargs = dict()

        if seed is not None:
            axelrod.seed(seed)

        player = self.player(**init_kwargs)

        match = axelrod.Match((player, opponent), turns=turns, noise=noise,
                              match_attributes=match_attributes)
        self.assertEqual(match.play(), expected_actions)

        if attrs:
            player = match.players[0]
            for attr, value in attrs.items():
                self.assertEqual(getattr(player, attr), value)

    def classifier_test(self, expected_class_classifier=None):
        """Test that the keys in the expected_classifier dictionary give the
        expected values in the player classifier dictionary. Also checks that
        two particular keys (memory_depth and stochastic) are in the
        dictionary."""
        player = self.player()

        # Test that player has same classifier as it's class unless otherwise
        # specified
        if expected_class_classifier is None:
            expected_class_classifier = player.classifier
        self.assertEqual(expected_class_classifier, self.player.classifier)

        self.assertTrue('memory_depth' in player.classifier,
                        msg="memory_depth not in classifier")
        self.assertTrue('stochastic' in player.classifier,
                        msg="stochastic not in classifier")
        for key in TestOpponent.classifier:
            self.assertEqual(
                player.classifier[key],
                self.expected_classifier[key],
                msg="%s - Behaviour: %s != Expected Behaviour: %s" %
                (key, player.classifier[key], self.expected_classifier[key]))


class TestMatch(unittest.TestCase):
    """Test class for heads up play between two given players. Plays an
    axelrod match between the two players."""

    def versus_test(self, player1, player2, expected_actions1,
                    expected_actions2, noise=None, seed=None):
        """Tests a sequence of outcomes for two given players."""
        if len(expected_actions1) != len(expected_actions2):
            raise ValueError("Mismatched History lengths.")
        if seed:
            axelrod.seed(seed)
        turns = len(expected_actions1)
        match = axelrod.Match((player1, player2), turns=turns, noise=noise)
        match.play()
        # Test expected sequence of play.
        for i, (outcome1, outcome2) in enumerate(
            zip(expected_actions1, expected_actions2)
        ):
            player1.play(player2)
            self.assertEqual(player1.history[i], outcome1)
            self.assertEqual(player2.history[i], outcome2)

    def test_versus_with_incorrect_history_lengths(self):
        """Test the error raised by versus_test if expected actions do not
        match up"""
        with self.assertRaises(ValueError):
            p1, p2 = axelrod.Cooperator(), axelrod.Cooperator()
            actions1 = [C, C]
            actions2 = [C]
            self.versus_test(p1, p2, actions1, actions2)


def test_four_vector(test_class, expected_dictionary):
    """
    Checks that two dictionaries match -- the four-vector defining
    a memory-one strategy and the given expected dictionary.
    """
    player1 = test_class.player()
    for key in sorted(expected_dictionary.keys(), key=str):
        test_class.assertAlmostEqual(
            player1._four_vector[key], expected_dictionary[key])
