import random
import unittest

import axelrod
from axelrod import DefaultGame, Player, simulate_play


C, D = axelrod.Actions.C, axelrod.Actions.D


def cooperate(self):
    return C

def defect(self):
    return D

def randomize(self):
    return random.choice([C, D])


class TestPlayerClass(unittest.TestCase):

    name = "Player"
    player = Player
    classifier = {
        'stochastic': False
    }

    def test_add_noise(self):
        random.seed(1)
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
        for h1, h2 in zip([C, C, D, D, C], [C, D, C, D, D]):
            simulate_play(player1, player2, h1, h2)
        self.assertEqual(dict(player1.state_distribution),
                         {(C, C): 1, (C, D): 2, (D, C): 1, (D, D): 1})
        self.assertEqual(dict(player2.state_distribution),
                         {(C, C): 1, (C, D): 1, (D, C): 2, (D, D): 1})

    def test_noisy_play(self):
        random.seed(1)
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
                   history2=None, random_seed=None, attrs=None):
    """
    Test responses to arbitrary histories. Used for the following tests
    in TestPlayer: first_play_test, second_play_test, and responses_test.
    Works for arbitrary players as well. Input response_lists is a list of
    lists, each of which consists of a list for the history of player 1, a
    list for the history of player 2, and a list for the subsequent moves
    by player one to test.
    """

    if random_seed is None:
        random_seed = 0
    axelrod.seed(random_seed)
    # Force the histories, In case either history is impossible or if some
    # internal state needs to be set, actually submit to moves to the strategy
    # method. Still need to append history manually.
    if history1 and history2:
        for h1, h2 in zip(history1, history2):
            simulate_play(player1, player2, h1, h2)
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
    "A Test class from which other player test classes are inherited"
    player = TestOpponent
    expected_class_classifier = None

    def test_initialisation(self):
        """Test that the player initiates correctly."""
        if self.__class__ != TestPlayer:
            player = self.player()
            self.assertEqual(player.history, [])
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

    def test_reset(self):
        """Override to make sure any internal variables are reset."""

    def test_reset_history(self):
        """Make sure history resetting works correctly, regardless
        if self.test_reset() is overwritten."""
        p = self.player()
        player2 = axelrod.Cooperator()
        for _ in range(10):
            p.play(player2)
        p.reset()
        self.assertEqual(len(p.history), 0)
        self.assertEqual(self.player().cooperations, 0)
        self.assertEqual(self.player().defections, 0)
        self.assertEqual(self.player().state_distribution, dict())

    def test_reset_clone(self):
        """Make sure history resetting with cloning works correctly, regardless
        if self.test_reset() is overwritten."""
        player = self.player()
        clone = player.clone()

        for k, v in clone.__dict__.items():
            self.assertEqual(v, getattr(clone, k))

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

    def first_play_test(self, play, random_seed=None):
        """Tests first move of a strategy."""
        player1 = self.player()
        player2 = TestOpponent()
        test_responses(self, player1, player2, play, random_seed=random_seed)

    def second_play_test(self, *responses, random_seed=None):
        """Test responses to the four possible one round histories. Input
        responses is simply the four responses to CC, CD, DC, and DD."""
        # Construct the test lists
        histories = [[C, C], [C, D], [D, C], [D, D]]
        for i, history in enumerate(histories):
            # Needs to be in the inner loop in case player retains some state
            player1 = self.player()
            player2 = TestOpponent()
            test_responses(self, player1, player2, responses[i], history[0],
                           history[1], random_seed=random_seed)

    def responses_test(self, responses, history1=None, history2=None,
                       random_seed=None, tournament_length=200, attrs=None,
                       init_args=(), init_kwargs=None):
        """Test responses to arbitrary histories. A match is played where the
        histories are enforced and the sequence of plays in responses is
        checked to be the outcome. Internal variables can be checked with the
        attrs attribute and arguments to the first player can be passed in
        init_args.

        Parameters
        ----------
        responses: History or sequence of axelrod.Actions
            The expected outcomes
        history1, history2: sequences of prior history to enforce
        random_seed: int
            A random seed if needed for reproducibility
        tournament_length: int
            Some players require the length of the match
        attrs: dict
            dictionary of internal attributes to check at the end of all plays
            in player
        init_args: tuple or list
            A list of arguments to instantiate player with
        init_kwargs: dictionary
            A list of keyword arguments to instantiate player with
        """
        if init_kwargs is None:
            init_kwargs = dict()
        player1 = self.player(*init_args, **init_kwargs)
        player1.match_attributes['length'] = tournament_length
        player2 = TestOpponent()
        player2.match_attributes['length'] = tournament_length
        test_responses(
            self, player1, player2, responses, history1, history2,
            random_seed=random_seed, attrs=attrs)

        # Test that we get the same sequence after a reset
        player1.reset()
        player2.reset()
        test_responses(
            self, player1, player2, responses, history1, history2,
            random_seed=random_seed, attrs=attrs)

        # Test that we get the same sequence after a clone
        player1 = player1.clone()
        player2 = player2.clone()
        test_responses(
            self, player1, player2, responses, history1, history2,
            random_seed=random_seed, attrs=attrs)

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


class TestHeadsUp(unittest.TestCase):
    """Test class for heads up play between two given players."""

    def versus_test(self, player_1, player_2, expected_actions1,
                    expected_actions2, random_seed=None):
        """Tests a sequence of outcomes for two given players."""
        if random_seed:
            random.seed(random_seed)
        # Test sequence of play
        for outcome_1, outcome_2 in zip(expected_actions1, expected_actions2):
            player_1.play(player_2)
            self.assertEqual(player_1.history[-1], outcome_1)
            self.assertEqual(player_2.history[-1], outcome_2)


def test_four_vector(test_class, expected_dictionary):
    """
    Checks that two dictionaries match -- the four-vector defining
    a memory-one strategy and the given expected dictionary.
    """
    player1 = test_class.player()
    for key in sorted(expected_dictionary.keys()):
        test_class.assertAlmostEqual(
            player1._four_vector[key], expected_dictionary[key])
