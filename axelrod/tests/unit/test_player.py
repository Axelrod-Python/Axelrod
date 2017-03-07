import random
import unittest
import warnings
import types

import numpy as np

import axelrod
from axelrod import DefaultGame, MockPlayer, Player, simulate_play


C, D = axelrod.Actions.C, axelrod.Actions.D


# Generic strategy functions for testing

def cooperate(*args):
    return C


def defect(*args):
    return D


def randomize(*args):
    return random.choice([C, D])


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
        player1, player2 = self.player(), self.player()
        player1.strategy = randomize
        player2.strategy = randomize
        history_1 = [C, C, D, D, C]
        history_2 = [C, D, C, D, D]
        for h1, h2 in zip(history_1, history_2):
            simulate_play(player1, player2, h1, h2)
        self.assertEqual(player1.state_distribution,
                         {(C, C): 1, (C, D): 2, (D, C): 1, (D, D): 1})
        self.assertEqual(player2.state_distribution,
                         {(C, C): 1, (C, D): 1, (D, C): 2, (D, D): 1})

    def test_noisy_play(self):
        axelrod.seed(1)
        noise = 0.2
        player1, player2 = self.player(), self.player()
        player1.strategy = cooperate
        player2.strategy = defect
        player1.play(player2, noise)
        self.assertEqual(player1.history[0], D)
        self.assertEqual(player2.history[0], D)

    def test_strategy(self):
        self.assertRaises(
            NotImplementedError, self.player().strategy, self.player())

    def test_clone(self):
        """Tests player cloning."""
        player1 = axelrod.Random(0.75)  # 0.5 is the default
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


def test_responses(test_class, player1, player2, responses, history1=None,
                   history2=None, seed=None, attrs=None):
    """
    Test responses to arbitrary histories. Used for the following tests
    in TestPlayer: first_play_test, second_play_test, and responses_test.
    Works for arbitrary players as well. Input response_lists is a list of
    lists, each of which consists of a list for the history of player 1, a
    list for the history of player 2, and a list for the subsequent moves
    by player one to test.
    """

    if seed is not None:
        axelrod.seed(seed)
    # Force the histories, In case either history is impossible or if some
    # internal state needs to be set, actually submit to moves to the strategy
    # method. Still need to append history manually.
    if history1 and history2:
        for h1, h2 in zip(history1, history2):
            s1, s2 = simulate_play(player1, player2, h1, h2)
    # Run the tests
    for response in responses:
        s1, s2 = simulate_play(player1, player2)
        test_class.assertEqual(s1, response)
    if attrs:
        for attr, value in attrs.items():
            test_class.assertEqual(getattr(player1, attr), value)


class TestOpponent(Player):
    """A player who only exists so we have something to test against"""

    name = 'TestPlayer'
    classifier = {
        'memory_depth': 0,
        'stochastic': False,
        'makes_use_of': None,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

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
        opponent = axelrod.Random()

        for seed in range(10):
            axelrod.seed(seed)
            player.play(opponent)

        player.reset()
        self.assertEqual(len(player.history), 0)
        self.assertEqual(player.cooperations, 0)
        self.assertEqual(player.defections, 0)
        self.assertEqual(player.state_distribution, dict())

        for attribute, reset_value in player.__dict__.items():
            original_value = getattr(clone, attribute)

            if isinstance(reset_value, np.ndarray):
                self.assertTrue(np.array_equal(reset_value, original_value),
                                msg=attribute)

            if isinstance(reset_value, types.GeneratorType):
                for _ in range(10):
                    self.assertEqual(next(reset_value),
                                     next(original_value), msg=attribute)
            else:
                self.assertEqual(reset_value, original_value, msg=attribute)

    def test_reset_clone(self):
        """Make sure history resetting with cloning works correctly, regardless
        if self.test_reset() is overwritten."""
        player = self.player()
        clone = player.clone()
        for attribute, value in player.__dict__.items():
            clone_value = getattr(player, attribute)
            if isinstance(value, np.ndarray):
                self.assertTrue(np.array_equal(value, clone_value),
                                msg=attribute)
            else:
                self.assertEqual(value, clone_value, msg=attribute)

    def test_clone(self):
        # Test that the cloned player produces identical play
        player1 = self.player()
        if str(player1) in ["Darwin", "Human"]:
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
                   axelrod.TitForTat(), axelrod.Random(r)]:
            player1.reset()
            player2.reset()
            seed = random.randint(0, 10 ** 6)
            for p in [player1, player2]:
                axelrod.seed(seed)
                m = axelrod.Match((p, op), turns=turns)
                m.play()
            self.assertEqual(len(player1.history), turns)
            self.assertEqual(player1.history, player2.history)

    def first_play_test(self, play, seed=None):
        """Tests first move of a strategy."""
        player1 = self.player()
        player2 = TestOpponent()
        test_responses(self, player1, player2, play, seed=seed)

    def second_play_test(self, rCC, rCD, rDC, rDD, seed=None):
        """Test responses to the four possible one round histories. Input
        responses is simply the four responses to CC, CD, DC, and DD."""
        # Test tests are likely to throw expected warnings.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_responses(self, self.player(), axelrod.Cooperator(),
                           rCC, C, C, seed=seed)
            test_responses(self, self.player(), axelrod.Defector(),
                           rCD, C, D, seed=seed)
            test_responses(self, self.player(), axelrod.Cooperator(),
                           rDC, D, C, seed=seed)
            test_responses(self, self.player(), axelrod.Defector(),
                           rDD, D, D, seed=seed)

    def versus_test(self, opponent, expected_outcomes,
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
        expected_outcomes: List
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

        turns = len(expected_outcomes)
        if init_kwargs is None:
            init_kwargs = dict()

        if seed is not None:
            axelrod.seed(seed)

        player = self.player(**init_kwargs)

        match = axelrod.Match((player, opponent), turns=turns, noise=noise,
                              match_attributes=match_attributes)
        self.assertEqual(match.play(), expected_outcomes)

        if attrs:
            player = match.players[0]
            for attr, value in attrs.items():
                self.assertEqual(getattr(player, attr), value)

    def responses_test(self, responses, player_history=None,
                       opponent_history=None, seed=None, length=200,
                       attrs=None,
                       init_args=None, init_kwargs=None):
        """Test responses to arbitrary histories. A match is played where the
        histories are enforced and the sequence of plays in responses is
        checked to be the outcome. Internal variables can be checked with the
        attrs attribute and arguments to the first player can be passed in
        init_args.

        Parameters
        ----------
        responses: History or sequence of axelrod.Actions
            The expected outcomes
        player_history, opponent_history: sequences of prior history to enforce
        seed: int
            A random seed if needed for reproducibility
        length: int
            Some players require the length of the match
        attrs: dict
            dictionary of internal attributes to check at the end of all plays
            in player
        init_args: tuple or list
            A list of arguments to instantiate player with
        init_kwargs: dictionary
            A list of keyword arguments to instantiate player with
        """
        if init_args is None:
            init_args = ()
        if init_kwargs is None:
            init_kwargs = dict()

        player1 = self.player(*init_args, **init_kwargs)
        player1.set_match_attributes(length=length)
        player2 = MockPlayer()
        player2.set_match_attributes(length=length)
        test_responses(self, player1, player2, responses, player_history,
                       opponent_history, seed=seed, attrs=attrs)

        # Test that we get the same sequence after a reset
        player1.reset()
        player2.reset()
        test_responses(self, player1, player2, responses, player_history,
                       opponent_history, seed=seed, attrs=attrs)

        # Test that we get the same sequence after a clone
        player1 = player1.clone()
        player2 = player2.clone()
        test_responses(self, player1, player2, responses, player_history,
                       opponent_history, seed=seed, attrs=attrs)

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
            zip(expected_actions1, expected_actions2)):
            player1.play(player2)
            self.assertEqual(player1.history[i], outcome1)
            self.assertEqual(player2.history[i], outcome2)


def test_four_vector(test_class, expected_dictionary):
    """
    Checks that two dictionaries match -- the four-vector defining
    a memory-one strategy and the given expected dictionary.
    """
    player1 = test_class.player()
    for key in sorted(expected_dictionary.keys()):
        test_class.assertAlmostEqual(
            player1._four_vector[key], expected_dictionary[key])
